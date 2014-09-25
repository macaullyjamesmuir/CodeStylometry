
import weka.classifiers.*;
import weka.classifiers.trees.RandomForest;
import weka.core.Instances;
import java.io.FileReader;
import java.util.*;

public class AuthorClassification {


	public static void main(String[] args) throws Exception 
	{

		int numberFiles=8;
		int seedNumber=7;
		int foldNumber=numberFiles;
		for(seedNumber=7; seedNumber<11; seedNumber++){
		String arffFile = "/Users/Aylin/Desktop/Drexel/2014/ARLInternship/SCAAarffs/mergedArffs/incremental/"+numberFiles+"files2014FS9Andrew.arff";		 
		RandomForest cls = new RandomForest();
		Instances data = new Instances(new FileReader(arffFile));
		data.setClassIndex(data.numAttributes() - 1);
		System.out.println("number of authors: " + data.numClasses());
		String[] options = weka.core.Utils.splitOptions("-I 300 -K 0 -S "+seedNumber);

		cls.setOptions(options);
		cls.buildClassifier(data);
		
		
	    Evaluation eval = new Evaluation(data);
	    eval.crossValidateModel(cls, data,foldNumber , new Random(seedNumber));
       // System.out.println(eval.toSummaryString("\nResults\n", true));
//        System.out.println(eval.fMeasure(1) + " " + eval.precision(1) + " " + eval.recall(1));
System.out.println("etsttet");
	        
	      
		}	 


	}
	
}