public class Laptop extends Computer {
    private double screenSize;

    public Laptop(double initPrice, int initQuantity, double initCPUSpeed, int initRAM, boolean initSSD, int initStorage, double initScreen) {
        super(initPrice, initQuantity, initCPUSpeed, initRAM, initSSD, initStorage);
        this.screenSize = initScreen;
    }

    public String toString() {
        double var10000 = this.screenSize;
        String result = "" + var10000 + " inch Laptop PC with " + this.getCPUSpeed() + "ghz CPU, " + this.getRAM() + "GB RAM, " + this.getStorage() + "GB ";
        if (this.getSSD()) {
            result = result + "SSD drive.";
        } else {
            result = result + "HDD drive.";
        }

        return result;
    }
}
