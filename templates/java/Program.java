import java.io.*;
import java.nio.file.*;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;

public class Program
{
	record Result(Integer part1, Integer part2) { }

	private static Integer part1(List<String> input)
	{
		return 1;
	}

	private static Integer part2(List<String> input)
	{
		return 2;
	}

	public static Result solve(List<String> input)
	{
		return new Result(part1(input), part2(input));
	}

	public static List<String> getInput(String filePath) throws FileNotFoundException, IOException
	{
		Path path = Paths.get(filePath);
		if (!Files.isRegularFile(path))
			throw new FileNotFoundException(filePath + "is not a valid input file path");

		return Files.readAllLines(path);
	}

	public static void main(String[] args) throws Exception
	{
		if (args.length == 0)
			throw new Exception("Please, add input file path as parameter");

		List<String> input = getInput(args[0]);
		long start = System.nanoTime();
		Result result = solve(input);
		long end = System.nanoTime();
		System.out.println("P1: " + result.part1);
		System.out.println("P2: " + result.part2);
		System.out.println(String.format("\nTime: %.7f", (end - start) * 1e-9));
	}
}
