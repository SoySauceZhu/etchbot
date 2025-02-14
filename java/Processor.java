import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.logging.Logger;

public class Processor {
    private static final Logger logger = Logger.getLogger(Processor.class.getName());

    public static BufferedImage resize(BufferedImage image, int width) {
        int originalWidth = image.getWidth();
        int originalHeight = image.getHeight();

        double scaleFactor = (double) width / originalWidth;
        int newWidth = (int) (originalWidth * scaleFactor);
        int newHeight = (int) (originalHeight * scaleFactor);

        BufferedImage resizedImage = new BufferedImage(newWidth, newHeight, BufferedImage.TYPE_BYTE_GRAY);
        resizedImage.getGraphics().drawImage(image, 0, 0, newWidth, newHeight, null);
        return resizedImage;
    }

    public static BufferedImage process(BufferedImage image) {
        logger.info("Starting image processing.");

        int width = image.getWidth();
        int height = image.getHeight();
        BufferedImage processedImage = new BufferedImage(width, height, BufferedImage.TYPE_BYTE_GRAY);

        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                Color color = new Color(image.getRGB(x, y));
                int gray = (color.getRed() + color.getGreen() + color.getBlue()) / 3;
                processedImage.setRGB(x, y, new Color(gray, gray, gray).getRGB());
            }
        }

        logger.info("Image processing complete.");
        return processedImage;
    }

    public static void saveImage(BufferedImage image, String path) {
        try {
            File output = new File(path);
            ImageIO.write(image, "jpg", output);
            logger.info("Image saved at: " + path);
        } catch (IOException e) {
            logger.severe("Failed to save image: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        try {
            BufferedImage inputImage = ImageIO.read(new File("resources/input.jpg"));
            BufferedImage resizedImage = resize(inputImage, 480);
            BufferedImage processedImage = process(resizedImage);
            saveImage(processedImage, "output/processed_image.jpg");
        } catch (IOException e) {
            logger.severe("Error reading input image: " + e.getMessage());
        }
    }
}
