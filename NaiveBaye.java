/**
 * Created with IntelliJ IDEA.
 * User: harryquigley  ciaraedwards
 * Date: 10/11/15
 * Time: 12:15
 */

//calculates probabilities for inmates with the target attributes of remorse, religion and denial.
package weka.classifiers;
import java.util.Enumeration;
import java.io.*;
import java.util.*;
import weka.core.*;
import weka.core.converters.ConverterUtils.DataSource;

public class NaiveBaye extends Classifier {

    //the count for the sentiment attribute
    private double [][][] counts;

    //Used to calculate the mean for each attribute
    private double [][] means;

    //as above but for standard deviation
    private double [][] stdDev;

    //Used to hold the probabilities for each class
    private double [] prior;

    //used to hold training attributes
    private Instances inst;

    //used in calculating normal distribution
    private static double NORM_CONST = Math.sqrt(2 * Math.PI);

    
	 //creates the classifier takes a set of training data as param
    public void buildClassifier(Instances instances) throws Exception {

        int index = 0;
        double sum;
		
		//check attributes in arff file are in correct format (nominal format)
        if (instances.checkForStringAttributes()) {
            throw new Exception("Can't handle string attributes!");
        }
        if (instances.classAttribute().isNumeric()) {
            throw new Exception("Naive Bayes: Class is numeric!");
        }

        inst = new Instances(instances, 0);

        // Reserves space
        counts = new double[instances.numClasses()]
                [instances.numAttributes() - 1][0];
        means = new double[instances.numClasses()]
                [instances.numAttributes() - 1];
        stdDev = new double[instances.numClasses()]
                [instances.numAttributes() - 1];
        prior = new double[instances.numClasses()];
		//creating an instance of Enumeration class to cycle through attributes
        Enumeration enum_ = instances.enumerateAttributes();
        while (enum_.hasMoreElements()) {
            Attribute attribute = (Attribute) enum_.nextElement();
			//checks its not the target attribute
            if (attribute.isNominal()) {
                for (int j = 0; j < instances.numClasses(); j++) {
                    counts[j][index] = new double[attribute.numValues()];
                }
			//increases the count value for the target attribute
            } else {
                for (int j = 0; j < instances.numClasses(); j++) {
                    counts[j][index] = new double[1];
                }
            }
            index++;
        }

        // Calculating sums and counts
        Enumeration enumInsts = instances.enumerateInstances();
        while (enumInsts.hasMoreElements()) {
            Instance instance = (Instance) enumInsts.nextElement();
			//checks for correlation
            if (!instance.classIsMissing()) {
                Enumeration enumAtts = instances.enumerateAttributes();
                index = 0;
                while (enumAtts.hasMoreElements()) {
                    Attribute attribute = (Attribute) enumAtts.nextElement();
                    if (!instance.isMissing(attribute)) {
                        if (attribute.isNominal()) {
                            counts[(int)instance.classValue()][index]
                                    [(int)instance.value(attribute)]++;
                        } else {
                            means[(int)instance.classValue()][index] +=
                                    instance.value(attribute);
                            counts[(int)instance.classValue()][index][0]++;
                        }
                    }
                    index++;
                }
                prior[(int)instance.classValue()]++;
            }
        }

        // Computing the means
        Enumeration enumAtts = instances.enumerateAttributes();
        index = 0;
        while (enumAtts.hasMoreElements()) {
            Attribute attribute = (Attribute) enumAtts.nextElement();
			//check for target attribute
            if (attribute.isNumeric()) {
                for (int j = 0; j < instances.numClasses(); j++) {
                    if (counts[j][index][0] < 2) {
						//makes sure pairing is possible
                        throw new Exception("attribute " + attribute.name() +
                                ": less than two values for class " +
                                instances.classAttribute().value(j));
                    }
                    means[j][index] /= counts[j][index][0];
                }
            }
            index++;
        }

        // Calculate the standard deviations for attributes
        enumInsts = instances.enumerateInstances();
        while (enumInsts.hasMoreElements()) {
            Instance instance =
                    (Instance) enumInsts.nextElement();
            if (!instance.classIsMissing()) {
                enumAtts = instances.enumerateAttributes();
                index = 0;
                while (enumAtts.hasMoreElements()) {
                    Attribute attribute = (Attribute) enumAtts.nextElement();
                    if (!instance.isMissing(attribute)) {
                        if (attribute.isNumeric()) {
                            stdDev[(int)instance.classValue()][index] +=
                                    (means[(int)instance.classValue()][index]-
                                            instance.value(attribute))*
                                            (means[(int)instance.classValue()][index]-
                                                    instance.value(attribute));
                        }
                    }
                    index++;
                }
            }
        }
		//standard deviation for classes of attributes
        enumAtts = instances.enumerateAttributes();
        index = 0;
        while (enumAtts.hasMoreElements()) {
            Attribute attribute = (Attribute) enumAtts.nextElement();
            if (attribute.isNumeric()) {
                for (int j = 0; j < instances.numClasses(); j++) {
                    if (stdDev[j][index] <= 0) {
                        throw new Exception("attribute " + attribute.name() +
                                ": standard deviation is 0 for class " +
                                instances.classAttribute().value(j));
                    }
                    else {
                        stdDev[j][index] /= counts[j][index][0] - 1;
                        stdDev[j][index] = Math.sqrt(stdDev[j][index]);
                    }
                }
            }
            index++;
        }

        // Grouping counts by simularities
        enumAtts = instances.enumerateAttributes();
        index = 0;
        while (enumAtts.hasMoreElements()) {
            Attribute attr = (Attribute) enumAtts.nextElement();
            if (attr.isNominal()) {
                for (int j = 0; j < instances.numClasses(); j++) {
                    sum = Utils.sum(counts[j][index]);
                    for (int i = 0; i < attr.numValues(); i++) {
                        counts[j][index][i] =
                                (counts[j][index][i] + 1)
                                        / (sum + (double)attr.numValues());
                    }
                }
            }
            index++;
        }

        // Normalizing probabilities for attrs
        sum = Utils.sum(prior);
        for (int j = 0; j < instances.numClasses(); j++)
            prior[j] = (prior[j] + 1)
                    / (sum + (double)instances.numClasses());
    }

	//calculates probabilities for test data, takes the instance to be classified
	//returns the probability of the predicted results for the test data
    public double[] distributionForInstance(Instance instance) throws Exception {

        double [] probs = new double[instance.numClasses()];
        int index;

        for (int j = 0; j < instance.numClasses(); j++) {
            probs[j] = 1;
            Enumeration enumAtts = instance.enumerateAttributes();
            index = 0;
            while (enumAtts.hasMoreElements()) {
                Attribute attr = (Attribute) enumAtts.nextElement();
                if (!instance.isMissing(attr)) {
                    if (attr.isNominal()) {
                        probs[j] *= counts[j][index][(int)instance.value(attr)];
                    } else {
                        probs[j] *= normalDens(instance.value(attr),
                                means[j][index],
                                stdDev[j][index]);}
                }
                index++;
            }
            probs[j] *= prior[j];
        }

        // Normalize probabilities
        Utils.normalize(probs);

        return probs;
    }

    //This class main purpose is to display the results generated
    public String toString() {

        if (inst == null) {
            return "Naive Bayes (simple): No model built yet.";
        }
        try {
            StringBuffer results = new StringBuffer("Naive Bayes (simple)");
            int index;

            for (int i = 0; i < inst.numClasses(); i++) {
                results.append("\n\nClass " + inst.classAttribute().value(i)
                        + ": P(C) = "
                        + Utils.doubleToString(prior[i], 10, 8)
                        + "\n\n");
                Enumeration enumAtts = inst.enumerateAttributes();
                index = 0;
                while (enumAtts.hasMoreElements()) {
                    Attribute attr = (Attribute) enumAtts.nextElement();
                    results.append("Attribute " + attr.name() + "\n");
                    if (attr.isNominal()) {
                        for (int j = 0; j < attr.numValues(); j++) {
                            results.append(attr.value(j) + "\t");
                        }
                        results.append("\n");
                        for (int j = 0; j < attr.numValues(); j++)
                            results.append(Utils.
                                    doubleToString(counts[i][index][j], 10, 8)
                                    + "\t");
                    } else {
                        results.append("Mean: " + Utils.
                                doubleToString(means[i][index], 10, 8) + "\t");
                        results.append("Standard Deviation: "
                                + Utils.doubleToString(stdDev[i][index], 10, 8));
                    }
                    results.append("\n\n");
                    index++;
                }
            }

            return results.toString();
        } catch (Exception e) {
            return "Unable to display Naive Bayes classifier!";
        }
    }

    //calculate normal distribution
    private double normalDens(double x, double mean, double stdDev) {

        double diff = x - mean;

        return (1 / (NORM_CONST * stdDev))
                * Math.exp(-(diff * diff / (2 * stdDev * stdDev)));
    }

    //creates instance of Classifier and calls evaluate on the
	//training and test files supplied in the cmd.
    public static void main(String [] argv) {

        Classifier scheme;

        try {
            scheme = new NaiveBaye();
            System.out.println(Evaluation.evaluateModel(scheme, argv));
        } catch (Exception e) {
            System.err.println(e.getMessage());
        }
    }
}


