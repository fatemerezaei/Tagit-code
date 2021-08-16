import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class EchoServer extends Thread {

    private DatagramSocket socket;
    private boolean running;
    private byte[] buf = new byte[500];
    static HashMap<String, Long> hm2 = new HashMap<String, Long>();
    //static ConcurrentHashMap<String, Long> hm2 = new ConcurrentHashMap<String, Long>();

    public EchoServer() {
        try {
            System.out.println(currentThread());
            socket = new DatagramSocket(4445);
        } catch (SocketException e) {
            e.printStackTrace();
        }
    }

    public void run() {
        running = true;
        DatagramPacket packet = new DatagramPacket(buf, buf.length);
        while (running) {
            try {
                socket.receive(packet);
                String time = new String(packet.getData(), 0, 25);
                hm2.put(time,System.nanoTime());
                if (hm2.size()>0 && hm2.size()%1000 == 0){
                    FileWriter fw = new FileWriter("times.txt", true);
                    BufferedWriter bw = new BufferedWriter(fw);
                    for(String s:hm2.keySet()){
                        bw.write(s);
                        bw.write(":");
                        bw.write(String.valueOf(hm2.get(s)));
                        bw.newLine();
                    }

                    bw.close();
                    hm2.clear();
                }
//                System.out.println(time);
//                System.out.println(System.nanoTime());
//                System.out.println(hm.size());
            } catch (IOException e) {
                e.printStackTrace();
            }
/*
            InetAddress address = packet.getAddress();
            int port = packet.getPort();
            packet = new DatagramPacket(buf, buf.length, address, port);
            String received = new String(packet.getData(), 0, packet.getLength());
            System.out.println(received);

            if (received.equals("end")) {
                running = false;
                continue;
            }
            try {
                String tmp = new String(packet.getData(), 0, packet.getLength())+"x";
                tmp+='x';


//                packet.setData((new String(packet.getData()) + "_Server").getBytes());
                packet.setData(tmp.getBytes());
                socket.send(packet);
            } catch (IOException e) {
                e.printStackTrace();
            }*/
        }
        socket.close();
    }
    public static void main(String[] args) {
        new EchoServer().start();
        new EchoServer().start();

    }
}

