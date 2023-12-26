//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by FernFlower decompiler)
//

import java.util.Iterator;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.Node;
import javafx.scene.control.Label;
import javafx.scene.control.ListView;
import javafx.scene.control.TextField;
import javafx.scene.layout.Pane;

public class ElectronicStoreView extends Pane {
    private Label label3 = new Label();
    private ListView<String> storeStockList;
    private ListView<String> currentCartList;
    private ListView<String> mostPopularItemsList;
    private TextField salesField;
    private TextField revenueField;
    private TextField dollarPerSaleField;
    private ButtonPane buttonPane;
    ObservableList<String> currentCart = FXCollections.observableArrayList();
    ObservableList<String> stock = FXCollections.observableArrayList();
    ObservableList<String> popularItems = FXCollections.observableArrayList();

    public ListView<String> getStoreStockList() {
        return this.storeStockList;
    }

    public ListView<String> getCurrentCartList() {
        return this.currentCartList;
    }

    public ButtonPane getButtonPane() {
        return this.buttonPane;
    }

    public void update(ElectronicStore model) {
        if (model.getCurrentCart().isEmpty()) {
            this.currentCart.clear();
        }

        int stockIndex;
        for(stockIndex = 0; stockIndex < model.getCurrentCart().size(); ++stockIndex) {
            if (model.getCurrentCart().get(stockIndex) != null) {
                ObservableList var10000;
                if (stockIndex < this.currentCart.size()) {
                    var10000 = this.currentCart;
                    String var10002 = String.valueOf(model.getCartQuantities().get(model.getCurrentCart().get(stockIndex)));
                    var10000.set(stockIndex, var10002 + "x " + ((Product)model.getCurrentCart().get(stockIndex)).toString());
                } else {
                    var10000 = this.currentCart;
                    String var10001 = String.valueOf(model.getCartQuantities().get(model.getCurrentCart().get(stockIndex)));
                    var10000.add(var10001 + "x " + ((Product)model.getCurrentCart().get(stockIndex)).toString());
                }
            } else if (stockIndex < this.currentCart.size()) {
                this.currentCart.remove(stockIndex);
                --stockIndex;
            }
        }

        Label var5 = this.label3;
        Object[] var6 = new Object[]{model.getCurrentTotal()};
        var5.setText("Current Cart: ($" + String.format("%.2f", var6) + ")");
        stockIndex = 0;
        Iterator var3 = model.getStock().iterator();

        Product i;
        while(var3.hasNext()) {
            i = (Product)var3.next();
            if (i != null && i.getStockQuantity() > 0) {
                if (stockIndex < this.stock.size()) {
                    this.stock.set(stockIndex, i.toString());
                } else {
                    this.stock.add(i.toString());
                }

                ++stockIndex;
            }
        }

        while(stockIndex < this.stock.size()) {
            this.stock.remove(stockIndex);
        }

        this.popularItems.clear();
        var3 = model.getMostPopularProducts().iterator();

        while(var3.hasNext()) {
            i = (Product)var3.next();
            if (i != null) {
                this.popularItems.add(i.toString());
            }
        }

        if (!this.currentCart.isEmpty()) {
            this.buttonPane.getBuyButton().setDisable(false);
        } else {
            this.buttonPane.getBuyButton().setDisable(true);
        }

        this.storeStockList.setItems(this.stock);
        this.mostPopularItemsList.setItems(this.popularItems);
        this.currentCartList.setItems(this.currentCart);
        this.salesField.setText(Integer.toString(model.getSales()));
        this.revenueField.setText(String.format("%.2f", model.getRevenue()));
        if (model.getSales() == 0) {
            this.dollarPerSaleField.setText("N/A");
        } else {
            this.dollarPerSaleField.setText(String.format("%.2f", model.getRevenue() / (double)model.getSales()));
        }

    }

    public ElectronicStoreView() {
        Label label1 = new Label("Store Summary:");
        label1.relocate(50.0, 45.0);
        Label label2 = new Label("Store Stock:");
        label2.relocate(300.0, 45.0);
        this.label3.setText("Current Cart: ($0.00)");
        this.label3.relocate(590.0, 45.0);
        Label label4 = new Label("#Sales:");
        label4.relocate(35.0, 70.0);
        Label label5 = new Label("Revenue:");
        label5.relocate(25.0, 100.0);
        Label label6 = new Label("$ / Sale:");
        label6.relocate(30.0, 130.0);
        Label label7 = new Label("Most Popular Items:");
        label7.relocate(35.0, 165.0);
        this.salesField = this.initTextField(90.0, 60.0);
        this.revenueField = this.initTextField(90.0, 95.0);
        this.dollarPerSaleField = this.initTextField(90.0, 125.0);
        this.storeStockList = this.initListView(190.0, 60.0, 290.0, 275.0);
        this.currentCartList = this.initListView(490.0, 60.0, 290.0, 275.0);
        this.mostPopularItemsList = this.initListView(10.0, 185.0, 175.0, 150.0);
        this.buttonPane = new ButtonPane();
        this.buttonPane.relocate(25.0, 340.0);
        this.buttonPane.setPrefSize(610.0, 40.0);
        this.getChildren().addAll(new Node[]{label1, label2, this.label3, label4, label5, label6, label7, this.salesField, this.revenueField, this.dollarPerSaleField, this.storeStockList, this.currentCartList, this.mostPopularItemsList, this.buttonPane});
        this.setPrefSize(800.0, 400.0);
    }

    private TextField initTextField(double x, double y) {
        TextField textField = new TextField();
        textField.relocate(x, y);
        textField.setPrefSize(95.0, 30.0);
        textField.setEditable(false);
        return textField;
    }

    private ListView<String> initListView(double x, double y, double width, double height) {
        ListView<String> listView = new ListView();
        listView.relocate(x, y);
        listView.setPrefSize(width, height);
        return listView;
    }
}