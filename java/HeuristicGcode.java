import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashSet;
import java.util.Set;
import java.util.Stack;
import java.util.logging.Logger;

public class HeuristicGcode {
    private static final Logger logger = Logger.getLogger(HeuristicGcode.class.getName());

    public static void generate(BufferedImage image, String gcodePath, double resizeFactor) {
        try {
            int width = image.getWidth();
            int height = image.getHeight();
            
            Set<String> pixelSet = new HashSet<>();
            for (int y = 0; y < height; y++) {
                for (int x = 0; x < width; x++) {
                    int pixel = image.getRGB(x, y) & 0xFF;
                    if (pixel > 127) {
                        pixelSet.add(x + "," + y);
                    }
                }
            }
            
            Set<String> visited = new HashSet<>();
            Stack<String> stack = new Stack<>();
            String startPixel = pixelSet.iterator().next();
            stack.push(startPixel);
            
            StringBuilder gcode = new StringBuilder();
            gcode.append("G21 ; Set units to mm\n");
            gcode.append("G90 ; Absolute positioning\n");
            
            try (FileWriter writer = new FileWriter(new File(gcodePath))) {
                while (!stack.isEmpty()) {
                    String currentPixel = stack.pop();
                    if (visited.contains(currentPixel)) continue;
                    visited.add(currentPixel);
                    
                    String[] parts = currentPixel.split(",");
                    int x = Integer.parseInt(parts[0]);
                    int y = Integer.parseInt(parts[1]);
                    gcode.append(String.format("G1 X%.2f Y%.2f F1000\n", x * resizeFactor, y * resizeFactor));
                    
                    for (int dx = -1; dx <= 1; dx++) {
                        for (int dy = -1; dy <= 1; dy++) {
                            if (dx == 0 && dy == 0) continue;
                            String neighbor = (x + dx) + "," + (y + dy);
                            if (pixelSet.contains(neighbor) && !visited.contains(neighbor)) {
                                stack.push(neighbor);
                            }
                        }
                    }
                }
                
                writer.write(gcode.toString());
            }
            
            logger.info("G-code successfully generated: " + gcodePath);
        } catch (IOException e) {
            logger.severe("Error generating G-code: " + e.getMessage());
        }
    }
}
