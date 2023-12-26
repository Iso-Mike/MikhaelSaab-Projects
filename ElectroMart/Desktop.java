public class Desktop extends Computer {
    private String towerProfile;

    public Desktop(double initPrice, int initQuantity, double initCPUSpeed, int initRAM, boolean initSSD, int initStorage, String initProfile) {
        super(initPrice, initQuantity, initCPUSpeed, initRAM, initSSD, initStorage);
        this.towerProfile = initProfile;
    }

    public String toString() {
        String var10000 = this.towerProfile;
        String result = var10000 + " Desktop PC with " + this.getCPUSpeed() + "ghz CPU, " + this.getRAM() + "GB RAM, " + this.getStorage() + "GB ";
        if (this.getSSD()) {
            result = result + "SSD drive.";
        } else {
            result = result + "HDD drive.";
        }

        return result;
    }
}
