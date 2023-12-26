import javafx.scene.Node;
import javafx.scene.control.Button;
import javafx.scene.layout.Pane;

public class ButtonPane extends Pane {
    private Button resetButton;
    private Button addButton;
    private Button removeButton;
    private Button buyButton;

    public Button getResetButton() {
        return this.resetButton;
    }

    public Button getAddButton() {
        return this.addButton;
    }

    public Button getRemoveButton() {
        return this.removeButton;
    }

    public Button getBuyButton() {
        return this.buyButton;
    }

    public ButtonPane() {
        Pane innerPane = new Pane();
        this.addButton = new Button("Add to Cart");
        this.addButton.relocate(265.0, 0.0);
        this.addButton.setPrefSize(145.0, 40.0);
        this.addButton.setDisable(true);
        this.removeButton = new Button("Remove from Cart");
        this.removeButton.relocate(465.0, 0.0);
        this.removeButton.setPrefSize(145.0, 40.0);
        this.removeButton.setDisable(true);
        this.buyButton = new Button("Complete Sale");
        this.buyButton.relocate(610.0, 0.0);
        this.buyButton.setPrefSize(145.0, 40.0);
        this.buyButton.setDisable(true);
        this.resetButton = new Button("Reset Store");
        this.resetButton.relocate(0.0, 0.0);
        this.resetButton.setPrefSize(145.0, 40.0);
        innerPane.getChildren().addAll(new Node[]{this.addButton, this.removeButton, this.buyButton, this.resetButton});
        this.getChildren().addAll(new Node[]{innerPane});
    }
}
