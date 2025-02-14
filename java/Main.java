import java.util.logging.Logger;

public class Main {
    private static final Logger logger = Logger.getLogger(Main.class.getName());

    public static void main(String[] args) {
        if (args.length < 3) {
            logger.severe("Usage: java Main <input_dir> <output_dir> <filename> [feed_rate] [resize_factor] [width]");
            return;
        }

        String inputDir = args[0];
        String outputDir = args[1];
        String filename = args[2];
        int feedRate = (args.length > 3) ? Integer.parseInt(args[3]) : 800;
        double resizeFactor = (args.length > 4) ? Double.parseDouble(args[4]) : 0.3;
        int width = (args.length > 5) ? Integer.parseInt(args[5]) : 480;

        GenerateController.imageToGcode(inputDir, outputDir, filename, feedRate, resizeFactor, width);
    }
}
