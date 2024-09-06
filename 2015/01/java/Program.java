import java.io.*;
import java.nio.file.*;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;

public class Program
{
	record Result(Integer part1, Integer part2) { }

	private static Integer part2(Integer[] directions) throws Exception
	{
		Integer currentFloor = 0;
		for (int index = 0; index < directions.length; index++)
		{
			currentFloor += directions[index];
			if (currentFloor == -1)
				return index + 1;
		}
		throw new Exception("Did not go below 0!");

	}

	public static Result solve(Integer[] directions) throws Exception
	{
		return new Result(Arrays.stream(directions).mapToInt(Integer::intValue).sum(), part2(directions));
	}

	public static Integer[] getInput(String filePath) throws FileNotFoundException, IOException
	{
		Path path = Paths.get(filePath);
		if (!Files.isRegularFile(path))
			throw new FileNotFoundException(filePath + "is not a valid input file path");

		List<Integer> directions = new ArrayList<Integer>();
		for (byte c: Files.readAllBytes(path))
			directions.add(c == '(' ? 1 : -1);
	
		return directions.toArray(new Integer[0]);	
	}

	public static void main(String[] args) throws Exception
	{
		if (args.length == 0)
			throw new Exception("Please, add input file path as parameter");

		Integer[] input = getInput(args[0]);
		long start = System.nanoTime();
		Result result = solve(input);
		long end = System.nanoTime();
		System.out.println("P1: " + result.part1);
		System.out.println("P2: " + result.part2);
		System.out.println(String.format("\nTime: %.7f", (end - start) * 1e-9));
	}
}
