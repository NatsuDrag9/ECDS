/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Shaurya Chauhan
 */
import java.awt.BorderLayout;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.SwingUtilities;

public class BrowseImg  {
    public BrowseImg(String filePath){
    SwingUtilities.invokeLater(new Runnable() {
   
    public void run(){
        JFrame frame= new JFrame(filePath); //title
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        BufferedImage img= null;
        try{
        img= ImageIO.read( new File(filePath));
        } catch (Exception e){
            e.printStackTrace();
            
        }
        
        JLabel lbl = new JLabel("ff");
        lbl.setIcon(new ImageIcon(img));
        frame.getContentPane().add(lbl, BorderLayout.CENTER);
        frame.pack();
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
         
    }});
    }
    public static void main(String args[]){
        final JFileChooser fc = new JFileChooser();
        int returnVal = fc.showOpenDialog(fc);
        String filePath= null;
        if (returnVal == JFileChooser.APPROVE_OPTION){
        filePath = fc.getSelectedFile().getAbsolutePath();
    }else{
            System.out.println("User CLicked Cancel");
            System.exit(1);
            }
    
    new BrowseImg(filePath);
    }
}