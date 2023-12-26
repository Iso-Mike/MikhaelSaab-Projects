//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by FernFlower decompiler)
//

import javafx.application.Application;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.Scene;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.Pane;
import javafx.stage.Stage;

public class ElectronicStoreApp extends Application {
    private ElectronicStore model = ElectronicStore.createStore();

    public ElectronicStoreApp() {
    }

    public void start(Stage stage) {
        Pane aPane = new Pane();
        final ElectronicStoreView view = new ElectronicStoreView();
        view.update(this.model);
        aPane.getChildren().add(view);
        view.getStoreStockList().setOnMousePressed(new EventHandler<MouseEvent>() {
            public void handle(MouseEvent mouseEvent) {
                if (!view.getStoreStockList().getSelectionModel().getSelectedItems().isEmpty()) {
                    view.getButtonPane().getAddButton().setDisable(false);
                }

            }
        });
        view.getCurrentCartList().setOnMousePressed(new EventHandler<MouseEvent>() {
            public void handle(MouseEvent mouseEvent) {
                view.getButtonPane().getRemoveButton().setDisable(view.getCurrentCartList().getSelectionModel().getSelectedItems().isEmpty());
            }
        });
        view.getButtonPane().getAddButton().setOnAction(new EventHandler<ActionEvent>() {
            public void handle(ActionEvent actionEvent) {
                ElectronicStoreApp.this.model.addToCart((Product)ElectronicStoreApp.this.model.getStock().get(view.getStoreStockList().getSelectionModel().getSelectedIndex()));
                view.update(ElectronicStoreApp.this.model);
            }
        });
        view.getButtonPane().getRemoveButton().setOnAction(new EventHandler<ActionEvent>() {
            public void handle(ActionEvent actionEvent) {
                ElectronicStoreApp.this.model.removeFromCart((Product)ElectronicStoreApp.this.model.getCurrentCart().get(view.getCurrentCartList().getSelectionModel().getSelectedIndex()));
                view.update(ElectronicStoreApp.this.model);
                view.getCurrentCartList().getSelectionModel().clearSelection();
                view.getButtonPane().getRemoveButton().setDisable(true);
            }
        });
        view.getButtonPane().getBuyButton().setOnAction(new EventHandler<ActionEvent>() {
            public void handle(ActionEvent actionEvent) {
                ElectronicStoreApp.this.model.Buy();
                view.update(ElectronicStoreApp.this.model);
            }
        });
        view.getButtonPane().getResetButton().setOnAction(new EventHandler<ActionEvent>() {
            public void handle(ActionEvent actionEvent) {
                ElectronicStoreApp.this.model = ElectronicStore.createStore();
                view.update(ElectronicStoreApp.this.model);
            }
        });
        stage.setTitle("Electronic Store Application");
        stage.setResizable(false);
        stage.setScene(new Scene(aPane));
        stage.show();
    }

    public static void main(String[] args) {
        Application.launch(args);
    }
}