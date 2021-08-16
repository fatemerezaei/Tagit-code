import java.io.IOException;
import java.net.*;
import java.security.NoSuchAlgorithmException;
import java.util.Date;
import java.util.concurrent.TimeUnit;

import static org.junit.Assert.assertEquals;

public class EchoClient {
    private DatagramSocket socket;
    private InetAddress address;

    private static int packetSize = 1000; //bytes
    private static byte[] buf = new byte[packetSize];


    public EchoClient() {
        try {
            socket = new DatagramSocket();
        } catch (SocketException e) {
            e.printStackTrace();
        }
        try {
            address = InetAddress.getByName("128.105.144.100");
//            address = InetAddress.getByName("localhost");
        } catch (UnknownHostException e) {
            e.printStackTrace();
        }
    }

    public String sendEcho(String msg) {
        //create 500 byte packet
        buf = msg.getBytes();
        DatagramPacket packet
                = new DatagramPacket(buf, buf.length, address, 4445);
        try {
            socket.send(packet);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return "";
//        packet = new DatagramPacket(buf, buf.length);
//        try {
//            socket.receive(packet);
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
//        String received = new String(
//                packet.getData(), 0, packet.getLength());
//        return received;
    }

    public void close() {
        socket.close();
    }

    public static void main(String[] args) {

/*        Date date = new Date();
        long nano_endTime = System.nanoTime();
        System.out.println(nano_endTime);
        int a=0;
        for(int i=0; i<1000000000; i++){
//            long timeMilli = date.getTime();
//            System.out.println(timeMilli);
            a++;

        }
        System.out.println(System.nanoTime()-nano_endTime);*/

        EchoClient client;
        client = new EchoClient();
        String time="";
        for(int i=1; i<10000; i+=2) {
            for(int j=0; j<2; j++){
                time = String.format("%020d", System.nanoTime());
                time=String.format("%05d", i+j) + time;
                System.out.println(time);
                time = String.format("%1$-" + packetSize + "s", time).replace(' ', '0');
                client.sendEcho(time);
            }

            try {
                TimeUnit.MILLISECONDS.sleep(20);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

        }
//        assertEquals("hello server", echo);



    }
}