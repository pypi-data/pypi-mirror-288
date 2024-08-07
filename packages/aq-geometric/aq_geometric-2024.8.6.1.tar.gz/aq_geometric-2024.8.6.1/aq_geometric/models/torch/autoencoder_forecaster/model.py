from datetime import datetime
from typing import List, Union, Optional, Dict, Tuple

import uuid
import os
import torch
import torch.nn.functional as F
import torch.optim as optim
import pandas as pd
import numpy as np
from torch.optim.lr_scheduler import ReduceLROnPlateau

import aq_geometric.metrics.metrics as aq_metrics
from aq_geometric.models.torch.base_model import TorchBaseModelAdapter
from aq_geometric.datasets.adapters.torch.aq_geometric_dataset import TorchGeometricDatasetAdapter
from aq_geometric.models.torch.autoencoder_forecaster.autoencoder import AqGeometricSpatioTemporalAutoencoder
from aq_geometric.models.torch.autoencoder_forecaster.forecaster import AutoencoderForecaster


class AqGeometricAutoEncoderForecaster(TorchBaseModelAdapter):
    r"""The .
    """
    def __init__(
        self,
        name: str = "AqGeometricAutoEncoderForecaster",
        guid: str = str(uuid.uuid4()),
        stations: Union[List, None] = None,
        features: List[str] = ["OZONE", "PM2.5", "NO2"],
        targets: List[str] = ["OZONE", "PM2.5", "NO2"],
        num_samples_in_node_feature: int = 48,
        num_samples_in_node_target: int = 12,
        is_iterative: bool = False,
        num_nodes: int = 5921,  # this is a fixed number for the BatchNorm1d layer
        hidden_dim: int = 256,
        latent_dim: int = 512,
        num_gru_layers: int = 2,
        bidirectional_gru: bool = True,
        device: Optional[str] = None,
        verbose: bool = False,
    ):
        super().__init__(
            name=name,
            guid=guid,
            stations=stations,
            features=features,
            targets=targets,
            num_samples_in_node_feature=num_samples_in_node_feature,
            num_samples_in_node_target=num_samples_in_node_target,
            is_iterative=is_iterative,
            verbose=verbose,
        )
        self.num_nodes = num_nodes
        self.num_features = len(features)
        self.hidden_dim = hidden_dim
        self.latent_dim = latent_dim
        self.num_gru_layers = num_gru_layers
        self.bidirectional_gru = bidirectional_gru
        self.device = torch.device(device) if device else torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.autoencoder_model = None
        self.model = None
  
    def save(self, path: str):
        """Save the model to a file."""
        assert self.model is not None, "the model must be trained or loaded before saving"
        # ensure the model is on the CPU
        self.model.cpu()
        if self.autoencoder_model is not None:
            self.autoencoder_model.cpu()

        # ensure the path exists
        # check if the path has a directory
        if os.path.dirname(path):
            # create the directory if it does not exist
            os.makedirs(os.path.dirname(path), exist_ok=True)

        # gather the model data
        model_data = {
            "name": self.name,
            "guid": self.guid,
            "stations": self.stations,
            "features": self.features,
            "targets": self.targets,
            "num_samples_in_node_feature": self.num_samples_in_node_feature,
            "num_samples_in_node_target": self.num_samples_in_node_target,
            "is_iterative": self.is_iterative,
            "num_nodes": self.num_nodes,
            "num_features": self.num_features,
            "hidden_dim": self.hidden_dim,
            "latent_dim": self.latent_dim,
            "num_gru_layers": self.num_gru_layers,
            "bidirectional_gru": self.bidirectional_gru,
            "state_dict": self.model.state_dict(),
            **self.kwargs
        }
        # save the model data
        torch.save(model_data, path)

    def load(self, path: str):
        """Load the model from a file."""
        # load the model data
        model_data = torch.load(path)

        # set the model data
        self.name = model_data["name"]
        self.guid = model_data["guid"]
        self.stations = model_data["stations"]
        self.features = model_data["features"]
        self.targets = model_data["targets"]
        self.num_samples_in_node_feature = model_data["num_samples_in_node_feature"]
        self.num_samples_in_node_target = model_data["num_samples_in_node_target"]
        self.num_features_in_node_feature = len(self.features)
        self.num_features_in_node_target = len(self.targets)
        self.is_iterative = model_data.get("is_iterative", False)  # for backwards compatibility
        
        # set the kwargs
        for key, value in model_data.items():
            if key not in ["name", "guid", "stations", "features", "targets", "num_samples_in_node_feature", "num_samples_in_node_target", "num_features_in_node_feature", "num_features_in_node_target", "is_iterative", "state_dict"]:
                setattr(self, key, value)

        autoencoder = AqGeometricSpatioTemporalAutoencoder(
            num_nodes=self.num_nodes,
            num_timestamps=self.num_samples_in_node_feature,
            num_features=self.num_features,
            hidden_dim=self.hidden_dim,
            latent_dim=self.latent_dim,
        )
        self.model = AutoencoderForecaster(autoencoder, forecast_steps=self.num_samples_in_node_target) 

        self.model.load_state_dict(model_data["state_dict"])
        self.model = self.model.to(self.device)

    def fit(
        self,
        train_set: TorchGeometricDatasetAdapter,
        val_set: Optional[TorchGeometricDatasetAdapter],
        batch_size: int = 32,
        n_epoch: int = 20,
        optimizer: Optional[torch.optim.Optimizer] = None,
        scheduler: Optional[torch.optim.lr_scheduler.ReduceLROnPlateau] = None,
        loss_fn: Optional[torch.nn.Module] = None,
        lr: float = 0.1,
        momentum: float = 0.9,
        verbose: bool = False,
        **kwargs
    ) -> None:
        """
        Trains or fine-tunes the model, handling either Dataset objects or iterators.
        
        Args:
            train_set (TorchGeometricDatasetAdapter): Training data.
            val_set (Optional[TorchGeometricDatasetAdapter]): Validation data.
            batch_size (int): Batch size for training.
            n_epoch (int): Number of training epochs.
            **kwargs: Additional training parameters (overrides defaults).
        """
        if self.autoencoder_model is None:
            # We train the AutoEncoder component once at initialization if no model is loaded from weights
            autoencoder_model = AqGeometricSpatioTemporalAutoencoder(
                num_nodes=self.num_nodes,
                num_timestamps=self.num_samples_in_node_feature,
                num_features=self.num_features,
                hidden_dim=self.hidden_dim,
                latent_dim=self.latent_dim,
            )
            autoencoder_model = autoencoder_model.to(self.device)
            
            if optimizer is None:
                optimizer = optim.SGD(autoencoder_model.parameters(), lr=lr, momentum=momentum)
            if scheduler is None:
                scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=1)
            if loss_fn is None:
                loss_fn = F.l1_loss
            best_val_loss = float('inf')  # Initialize best validation loss

            for epoch in range(n_epoch):
                autoencoder_model.train()
                epoch_loss = 0  # Track loss for the entire epoch
                count = 0

                for batch_indices in self.shuffle_in_batches(train_set, batch_size=batch_size):
                    for i in batch_indices:
                        graph = train_set.get(i)
                        if graph is None: 
                            continue
                        graph = self.transform_graph(graph)
                        graph = graph.to(self.device)

                        optimizer.zero_grad()

                        out, _ = autoencoder_model(graph.x, graph.edge_index, graph.x_mask)
                        pred = out[graph.x_mask]
                        true = graph.x[graph.x_mask]

                        loss = loss_fn(pred, true)
                        loss.backward()
                        optimizer.step()

                        epoch_loss += loss.item()
                        count += 1

                        if count % 100 == 0:
                            if verbose: print(f"Epoch {epoch}, Batch {count}, Avg. Loss: {epoch_loss / count:.4f}")

                epoch_loss_avg = epoch_loss / len(train_set) 
                if verbose: print(f"Epoch {epoch} finished. Avg. Loss: {epoch_loss_avg:.4f}")

                # Evaluation
                autoencoder_model.eval()
                avg_val_loss = 0
                with torch.no_grad():
                    for j in range(len(val_set)):
                        graph = val_set.get(j)
                        if graph is None:
                            continue
                        graph = self.transform_graph(graph)
                        graph = graph.to(self.device)
                        out, _ = autoencoder_model(graph.x, graph.edge_index, graph.x_mask)
                        pred = out[graph.x_mask]
                        val_loss = loss_fn(pred, graph.x[graph.x_mask])
                        avg_val_loss += val_loss.item()

                avg_val_loss /= len(val_set)
                
                # Update learning rate scheduler
                scheduler.step(avg_val_loss) 

                if avg_val_loss < best_val_loss:
                    best_val_loss = avg_val_loss
                    if verbose: print(f"New best model found with val loss {avg_val_loss:.4f}")
                    torch.save(autoencoder_model.state_dict(), "autoencoder_best_model.pt")
            
            # load the best model and save it, removing the temporary file afterwards
            autoencoder_model = AqGeometricSpatioTemporalAutoencoder(
                num_nodes=self.num_nodes,
                num_timestamps=self.num_samples_in_node_feature,
                num_features=self.num_features,
                hidden_dim=self.hidden_dim,
                latent_dim=self.latent_dim,
            )
            autoencoder_model.load_state_dict(torch.load("autoencoder_best_model.pt"))
            autoencoder_model = autoencoder_model.to(self.device)
            self.autoencoder_model = autoencoder_model
            os.remove("autoencoder_best_model.pt")

        if self.model is None:
            model = AutoencoderForecaster(self.autoencoder_model, forecast_steps=self.num_samples_in_node_target) 
            model = model.to(self.device)
            
            if optimizer is None:
                optimizer = optim.SGD(autoencoder_model.parameters(), lr=lr, momentum=momentum)
            if scheduler is None:
                scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=1)
            if loss_fn is None:
                loss_fn = F.l1_loss
        best_val_loss = float('inf')  # Initialize best validation loss

        for epoch in range(n_epoch):
            model.train()
            epoch_loss = 0  # Track loss for the entire epoch
            count = 0

            for batch_indices in self.shuffle_in_batches(train_set, batch_size=batch_size):
                for i in batch_indices:
                    graph = train_set.get(i)
                    if graph is None: 
                        continue
                    graph = self.transform_graph(graph)
                    graph = graph.to(self.device)

                    optimizer.zero_grad()

                    out = model(graph.x, graph.edge_index, graph.x_mask)
                    pred = out[graph.y_mask]
                    true = graph.y[graph.y_mask]

                    loss = loss_fn(pred, true)
                    loss.backward()
                    optimizer.step()

                    epoch_loss += loss.item()
                    count += 1

                    if count % 100 == 0:
                        if verbose: print(f"Epoch {epoch}, Batch {count}, Avg. Loss: {epoch_loss / count:.4f}")

            epoch_loss_avg = epoch_loss / len(train_set) 
            if verbose: print(f"Epoch {epoch} finished. Avg. Loss: {epoch_loss_avg:.4f}")

            # Evaluation
            model.eval()
            avg_val_loss = 0
            with torch.no_grad():
                for j in range(len(val_set)):
                    graph = val_set.get(j)
                    if graph is None:
                        continue
                    graph = self.transform_graph(graph)
                    graph = graph.to(self.device)
                    out = model(graph.x, graph.edge_index, graph.x_mask)
                    pred = out[graph.y_mask]
                    val_loss = loss_fn(pred, graph.y[graph.y_mask])
                    avg_val_loss += val_loss.item()

            avg_val_loss /= len(val_set)
            
            # Update learning rate scheduler
            scheduler.step(avg_val_loss) 

            if avg_val_loss < best_val_loss:
                best_val_loss = avg_val_loss
                if verbose: print(f"New best model found with val loss {avg_val_loss:.4f}")
                torch.save(model.state_dict(), "forecaster_best_model.pt")

        # load the best model and save it, removing the temporary file afterwards
        model = AutoencoderForecaster(self.autoencoder_model, forecast_steps=self.num_samples_in_node_target)
        model.load_state_dict(torch.load("forecaster_best_model.pt"))
        model = model.to(self.device)
        self.model = model
        os.remove("forecaster_best_model.pt")

    
    def predict(
        self,
        graph: "torch_geometric.data.Data",
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Predicts target values for the given dataset using the trained model.

        Args:
            graph (torch_geometric.data.Data): The input graph for prediction.

        Returns:
            Tuple[np.ndarray, np.ndarray]: A tuple containing the h3_indices and the predictions.
        """
        assert self.model is not None, "model must be fit before using `predict` or `evaluate`"

        graph = graph.to(self.device)
        graph = self.transform_graph(graph)

        out = self.model(graph.x, graph.edge_index, graph.x_mask)
        h3_index = graph.h3_index

        out = self.inverse_transform_predictions(out, graph)

        # ensure that out and h3_index are numpy ndarrays
        out = out.cpu().detach().numpy()
        if not (isinstance(h3_index, np.ndarray) or isinstance(h3_index, np.array)):
            h3_index = h3_index.cpu().detach().numpy()
        
        return h3_index, out

    def evaluate(
        self,
        dataset: TorchGeometricDatasetAdapter,
        metrics: List[str] = ["rmse", "mae"],
    ) -> Dict[str, float]:
        """Evaluates the model on the given dataset.

        Args:
            dataset (Union[AqGeometricInMemoryDataset, AqGeometricDataset]): Dataset for evaluation.
            metrics (List[str]): List of evaluation metrics to compute (the names of functions from the aq_geometric.metrics.metrics module).

        Returns:
            Dict[str, float]: A dictionary containing the computed evaluation metrics.
        """
        evaluation_results = {t: {m: [] for m in metrics} for t in self.targets}
        metric_fns = {m: getattr(aq_metrics, m) for m in metrics}

        for j in range(len(dataset)):
            g = dataset.get(j)
            if g is None: continue

            g = self.transform_graph(g)
            g = g.to(self.device)
            y = g.y
            y_mask = g.y_mask

            pred = self.model(g.x, g.edge_index, g.x_mask)

            pred = self.inverse_transform_predictions(pred, g)
            g = self.inverse_transform_graph(g)

      
            for i, t in enumerate(self.targets):
                y_masked = y[:, 0, i][y_mask[:, 0, i]].cpu().detach().numpy()
                pred_masked = pred[:, 0, i][y_mask[:, 0, i]].cpu().detach().numpy()
                for m in metrics:
                    evaluation_results[t][m].append(
                        metric_fns[m](y_masked, pred_masked)  # Calculate metric on masked values
                    )

        return evaluation_results

    def generate_forecasts(
        self,
        graph: "torch_geometric.data.Data",
        n_forecast_timesteps: int = 12,
        targets: Union[List[str], None] = None,
        verbose: Union[List[str], None] = None,
    ) -> Dict[str, pd.DataFrame]:
        """
        Generate forecasts using the loaded model.
        
        Args:
            graph (torch_geometric.data.Data): The graph data dictionary.
            n_forecast_timesteps (int, optional): Number of timesteps to forecast.
            targets (List[str], optional): List of targets to predict. If None, uses self.targets.
            verbose (List[str], optional): Verbosity levels. If None, uses self.verbose.

        Returns:
            Dict[str, pd.DataFrame]: A dictionary containing the forecasts for each target.
        """
        return self._generate_forecasts_direct(
            graph=graph,
            n_forecast_timesteps=n_forecast_timesteps,
            targets=targets if targets is not None else self.targets,
            verbose=verbose if verbose is not None else self.verbose)


    def transform_graph(self, graph: "torch_geometric.data.Data") -> "torch_geometric.data.Data":
        """
        Transform the input graph data for the model.

        Args:
            graph (Data): The input graph data.

        Returns:
            Data: The transformed graph data.
        """
        # For the GCN, the edge index must be long and the x and x_mask must be float32
        x = graph.x.to(torch.float32)
        y = graph.y.to(torch.float32)
        edge_index = graph.edge_index.to(torch.long)

        # update the x_mask to also mask o values
        x_mask = graph.x_mask
        y_mask = graph.y_mask

        # x_mask is bool valued, we wnt to update the indices in which x has a zero value to False
        x_mask = torch.where(x <= 0, torch.tensor(False), x_mask)
        y_mask = torch.where(graph.y <= 0, torch.tensor(False), y_mask)

        # Min-Max Scaling (Normalization)
        min_val = torch.min(x[graph.x_mask])
        max_val = torch.max(x[graph.x_mask])
        x_scaled = (x - min_val) / (max_val - min_val)
        y_scaled = (y - min_val) / (max_val - min_val)

        # Apply mask after scaling (to avoid scaling NaN values)
        x_scaled_masked = x_scaled * x_mask
        y_scaled_masked = y_scaled * y_mask

        # Save the min and max as graph attributes
        graph.x = x_scaled_masked
        graph.y = y_scaled_masked
        graph.x_mask = x_mask
        graph.y_mask = y_mask
        graph.edge_index = edge_index
        graph.x_min = min_val
        graph.x_max = max_val

        return graph

    def inverse_transform_graph(self, graph: "torch_geometric.data.Data") -> "torch_geometric.data.Data":
        """
        Inverse transform the input graph data for the model.

        Args:
            graph (Data): The input graph data.

        Returns:
            Data: The inverse transformed graph data.
        """
        graph.x *= (graph.x_max - graph.x_min) + graph.x_min
        graph.y *= (graph.x_max - graph.x_min) + graph.x_min

        return graph

    def inverse_transform_predictions(self, predictions: torch.Tensor, graph: Optional["torch_geometric.data.Data"] = None) -> torch.Tensor:
        """
        Inverse transform the predictions.

        Args:
            predictions (torch.Tensor): The predictions to inverse transform.
            graph optional(torch_geometric.data.Data): The 
        Returns:
            torch.Tensor: The inverse transformed predictions.
        """
        predictions *= (graph.x_max - graph.x_min) + graph.x_min
        
        return predictions
    
    def _generate_forecasts_direct(
        self,
        graph: "torch_geometric.data.Data",
        n_forecast_timesteps: int = 12,
        targets: Union[List[str], None] = None,
        verbose: Union[List[str], None] = None,
    ) -> Dict[str, pd.DataFrame]:
        """
        Generate forecasts using the loaded model.
        
        Args:
            graph (torch_geometric.data.Data): The graph data object.
            n_forecast_timesteps (int, optional): Number of timesteps to forecast.
            targets (List[str], optional): List of targets to predict. If None, uses self.targets.
            verbose (List[str], optional): Verbosity levels. If None, uses self.verbose.

        Returns:
            Dict[str, pd.DataFrame]: A dictionary containing the forecasts for each target.
        """
        h3_indices = graph.h3_index
        target_timestamps = graph.target_timestamps

        if not (isinstance(h3_indices, np.ndarray) or isinstance(h3_indices, np.array)):
            h3_indices = h3_indices.cpu().detach().numpy()
        if not (isinstance(target_timestamps, np.ndarray) or isinstance(target_timestamps, np.array)):
            target_timestamps = target_timestamps.cpu().detach().numpy()
        
        series = pd.Series(pd.to_datetime(target_timestamps))
        inferred_freq = pd.infer_freq(series)
        
        timestamps = pd.date_range(start=series[0], periods=n_forecast_timesteps, freq=inferred_freq)

        if verbose:
            print(
                f"[{datetime.now()}] generating forecasts for {len(h3_indices)} h3 indices and {len(timestamps)} timestamps"
            )

        valid_h3_indices, preds = self.predict(graph)

        if verbose:
            print(
                f"[{datetime.now()}] model generating forecasts for {len(valid_h3_indices)} valid h3 indices and {len(timestamps)} timestamps"
            )

        # prepare the forecasts
        target_dfs = {}
        for i, target in enumerate(targets):
            
            if verbose:
                print(f"[{datetime.now()}] preparing forecast for {target}")
            
            forecast_df = pd.DataFrame(
                preds[:, :, i], columns=timestamps,
                index=valid_h3_indices)
            
            if verbose:
                print(
                    f"[{datetime.now()}] forecast df shape for {target}: {forecast_df.shape}"
                )
            
            target_dfs[target] = forecast_df
            
            if verbose:
                print(f"[{datetime.now()}] added DataFrame {forecast_df.shape}")

        return target_dfs
