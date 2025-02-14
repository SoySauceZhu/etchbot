import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.logging.Logger;

public class GenerateController {
    private static final Logger logger = Logger.getLogger(GenerateController.class.getName());
    
    public static void imageToGcode(String inputDir, String outputDir, String filename, int feedRate, double resizeFactor, int width) {
        try {
            Files.createDirectories(Paths.get(inputDir));
            Files.createDirectories(Paths.get(outputDir));
            
            String filenameWithoutExt = filename.substring(0, filename.lastIndexOf('.'));
            
            File inputFile = new File(inputDir + File.separator + filename);
            File imageOutputFile = new File(outputDir + File.separator + "processed_" + filenameWithoutExt + ".jpg");
            File gcodeOutputFile = new File(outputDir + File.separator + "heuristic_" + filenameWithoutExt + ".gcode");
            
            BufferedImage inputImage = ImageIO.read(inputFile);
            inputImage = Processor.resize(inputImage, width);
            BufferedImage processedImage = Processor.process(inputImage);
            
            ImageIO.write(processedImage, "jpg", imageOutputFile);
            
            HeuristicGcode.generate(processedImage, gcodeOutputFile.getAbsolutePath(), resizeFactor, feedRate);
            
            logger.info("G-code generation complete.");
        } catch (IOException e) {
            logger.severe("Error processing image: " + e.getMessage());
        }
    }
    
    public static void main(String[] args) {
        String filename = "konan.jpg";
        imageToGcode("resources", "output", filename, 800, 0.3, 480);
    }
}
