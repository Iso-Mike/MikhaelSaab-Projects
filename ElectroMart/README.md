# ElectroMart Storefront

## Overview
ElectroMart Storefront is a comprehensive JavaFX application designed to manage an electronic store. The application provides functionalities for product management, sales tracking, and customer interaction through an intuitive graphical user interface.

## Features
- **Product Management:** Supports various product types like laptops, fridges, and toaster ovens, each with unique attributes.
- **Dynamic Storefront Interface:** Interactive JavaFX user interface for managing store inventory and customer shopping carts.
- **Sales and Revenue Tracking:** Monitors sales transactions, revenue generation, and popular products.
- **Modular Design:** Utilizes object-oriented principles for easy maintenance and scalability.

## Source Files
- `Appliance.java`, `Computer.java`, `Product.java`: Abstract base classes for different product categories.
- `Desktop.java`, `Fridge.java`, `Laptop.java`, `ToasterOven.java`: Concrete product classes representing specific items in the store.
- `ElectronicStore.java`: Core class for store management functionalities.
- `ElectronicStoreApp.java`: Main JavaFX application class that integrates the model with the UI.
- `ElectronicStoreView.java`: JavaFX view class for rendering the user interface.
- `ButtonPane.java`: Custom JavaFX pane for interactive buttons.

## How to Compile and Run
- **Compilation:** Use a Java compiler like `javac` to compile all the `.java` files. Ensure JavaFX libraries are included in the classpath.
- **Execution:** Run the `ElectronicStoreApp` class.

## Usage Instructions
1. **Start the Application:** Execute the `ElectronicStoreApp` class to launch the application.
2. **Navigate the Interface:** Use the graphical interface to add or remove products, manage inventory, and simulate sales.
3. **Track Store Performance:** Monitor sales, revenue, and popular products through the interface.

## Additional Information
- Ensure JavaFX SDK is properly set up in your development environment.
- This application follows the MVC pattern for clear separation of concerns and ease of future enhancements.
