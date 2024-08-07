import torch
import torch.nn as nn

from aq_geometric.models.torch.autoencoder_forecaster.autoencoder import AqGeometricSpatioTemporalAutoencoder


class AutoencoderForecaster(nn.Module):
    def __init__(self, autoencoder: AqGeometricSpatioTemporalAutoencoder, forecast_steps: int, num_gru_layers: int = 2, bidirectional_gru: bool = True):
        super().__init__()
        self.autoencoder = autoencoder
        self.forecast_steps = forecast_steps
        self.bidirectional_gru = bidirectional_gru

        # Freeze the weights of the autoencoder
        for param in self.autoencoder.parameters():
            param.requires_grad = False

        # Learnable layers for the forecaster (no gradients in the autoencoder's decoder)
        self.rnn_decoder = nn.GRU(
            input_size=self.autoencoder.decoder.fc2.out_features,  # Input from the latent adjustment layer
            hidden_size=self.autoencoder.decoder.rnn_decoder.hidden_size,  
            num_layers=num_gru_layers,
            batch_first=True,
            bidirectional=bidirectional_gru
        )
        self.gru_output_adjustment = nn.Linear(
            self.autoencoder.decoder.rnn_decoder.hidden_size * 2 if bidirectional_gru else self.autoencoder.decoder.rnn_decoder.hidden_size,
            self.autoencoder.decoder.rnn_decoder.hidden_size
        )
        self.latent_adjustment = nn.Linear(self.autoencoder.encoder.latent_dim, self.autoencoder.encoder.latent_dim)
        self.output_refinement = nn.Linear(self.autoencoder.decoder.fc3.out_features, self.autoencoder.decoder.fc3.out_features)

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor, x_mask: torch.Tensor):
        # Encode input to latent space (no gradients needed)
        with torch.no_grad():
            z = self.autoencoder.encoder(x, edge_index, x_mask)

        # Adjust latent representation
        z = self.latent_adjustment(z)
        hidden_decoded = self.autoencoder.decoder.fc2(z)

        # Reshape hidden states to be 2D for the first iteration
        hidden_dim_0 = self.autoencoder.num_features * 2 if self.bidirectional_gru else self.autoencoder.num_features
        h0 = hidden_decoded.unsqueeze(0).repeat(hidden_dim_0, 1, 1)
        # Expected shapes of h0: (hidden_dim_0, num_nodes, hidden_dim)

        # Get node mask from x_mask
        x_mask_temporal_mean = x_mask.to(torch.float32).mean(dim=-1)
        node_mask = x_mask_temporal_mean.any(dim=-1)
        # Expected shape of node_mask: (num_nodes,)

        # Forecast
        outputs = []
        for _ in range(self.forecast_steps):
            output, h0 = self.rnn_decoder(hidden_decoded.unsqueeze(1), h0)
            output = output.squeeze(0)
            # Expected shape of output: (num_nodes, 2 * hidden_dim)

            # Update the hidden state for the next step
            if self.bidirectional_gru:
                h0_forward, h0_backward = h0.chunk(2, 0)  # Split into forward and backward hidden states
                h0 = torch.cat((h0_forward, h0_backward), dim=0)  # Concatenate along the feature dimension
            else:
                h0 = h0.squeeze(0)

            # Adjust GRU output dimension before spatial refinement
            output = self.gru_output_adjustment(output.squeeze(0))
            # Expected shape of output: (num_nodes, hidden_dim)

            expanded_node_mask = node_mask.unsqueeze(1).unsqueeze(-1).expand_as(output) 
            output *= expanded_node_mask
            output_masked = torch.where(torch.isnan(output), torch.tensor(0.0), output)
            # Expected shape of output: (num_nodes, hidden_dim)

        
            output_masked = output_masked.permute(1, 0, 2)
            spatial_embeddings = self.autoencoder.decoder.gcn_decoder(output_masked, edge_index)  # (num_nodes, 1, hidden_dim)
            spatial_embeddings = spatial_embeddings.permute(1, 0, 2)

            # Update hidden_decoded for next step
            hidden_decoded = spatial_embeddings.squeeze(1)

            # Map to output features and refine
            output_features = self.output_refinement(self.autoencoder.decoder.fc3(spatial_embeddings))
            outputs.append(output_features)
            # Expected shape of output_features: (num_nodes, 1, num_features)

        # Combine outputs and return
        x_hat = torch.cat(outputs, dim=1)

        return x_hat
