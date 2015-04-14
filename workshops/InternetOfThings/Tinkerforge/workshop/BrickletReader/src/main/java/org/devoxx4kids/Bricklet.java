package org.javaland4kids;

/**
 * Created by alexanderbischof on 23.09.14.
 */
public class Bricklet {
    private String name;
    private String uid;

    public Bricklet(String name, String uid) {
        this.name = name;
        this.uid = uid;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getUid() {
        return uid;
    }

    public void setUid(String uid) {
        this.uid = uid;
    }

    @Override
    public String toString() {
        return "Bricklet{" +
                "name='" + name + '\'' +
                ", uid='" + uid + '\'' +
                '}';
    }
}
