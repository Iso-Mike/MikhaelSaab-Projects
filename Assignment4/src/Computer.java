//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by FernFlower decompiler)
//

public abstract class Computer extends Product {
    private double cpuSpeed;
    private int ram;
    private boolean ssd;
    private int storage;

    public Computer(double initPrice, int initQuantity, double initCPUSpeed, int initRAM, boolean initSSD, int initStorage) {
        super(initPrice, initQuantity);
        this.cpuSpeed = initCPUSpeed;
        this.ram = initRAM;
        this.ssd = initSSD;
        this.storage = initStorage;
    }

    public double getCPUSpeed() {
        return this.cpuSpeed;
    }

    public int getRAM() {
        return this.ram;
    }

    public boolean getSSD() {
        return this.ssd;
    }

    public int getStorage() {
        return this.storage;
    }
}