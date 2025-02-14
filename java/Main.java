import java.util.logging.Logger;

public class Main {
    private static final Logger logger = Logger.getLogger(Main.class.getName());

    public static void main(String[] args) {
        if (args.length < 3) {
            logger.severe("Usage: java Main <input_dir> <output_dir> <filename> [resize_factor] [width] [height]");
            return;
        }
        
        String inputDir = args[0];
        String outputDir = args[1];
        String filename = args[2];
        double resizeFactor = (args.length > 3) ? Double.parseDouble(args[3]) : 0.3;
        int width = (args.length > 4) ? Integer.parseInt(args[4]) : 480;
        Integer height = (args.length > 5) ? Integer.parseInt(args[5]) : null;
        
        GenerateController.imageToGcode(inputDir, outputDir, filename, resizeFactor, width, height);
    }
}
