/**
 * Created with IntelliJ IDEA.
 * User: harryquigley & ciaraedwards
 * Date: 03/11/15
 * Time: 03:24
 * To change this template use File | Settings | File Templates.
 */

/*Weka libraray is used to create a decision tree for remorse, religion and denial*/

import java.io.BufferedReader;
import java.io.FileReader;
import weka.classifiers.meta.FilteredClassifier;
import weka.classifiers.trees.DecisionStump;
import weka.classifiers.trees.J48;
import weka.classifiers.trees.RandomForest;
import weka.classifiers.trees.RandomTree;
import weka.core.Instances;
import weka.filters.unsupervised.attribute.Remove;
import weka.filters.unsupervised.attribute.NumericToNominal;
import java.awt.BorderLayout;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.BufferedReader;
import java.io.FileReader;
import weka.filters.Filter;
import javax.swing.JFrame;
import weka.classifiers.trees.J48;
import weka.core.Instances;
import weka.gui.treevisualizer.PlaceNode2;
import weka.gui.treevisualizer.TreeVisualizer;

public class DecisionTree {

    public static void main(String[] args) throws Exception {
        // Create training data instance
        Instances training_data = new Instances(
                new BufferedReader(
                        new FileReader(
                                "/Users/harryquigley/Desktop/College/4th Year/Data Warehousing & Data Mining/assignment/DeathRow-Data-Mining/finaldbofalltime.arff")));
        training_data.setClassIndex(training_data.numAttributes() - 4);
        // Create testing data instance
        Instances testing_data = new Instances(
                new BufferedReader(
                        new FileReader(
                                "/Users/harryquigley/Desktop/College/4th Year/Data Warehousing & Data Mining/assignment/DeathRow-Data-Mining/test_data.arff")));
        testing_data.setClassIndex(training_data.numAttributes() - 4);

        // Print initial data summary
        String summary = training_data.toSummaryString();

        int sampleNum = training_data.numInstances();

        int attrSampleNum = training_data.numAttributes();
        System.out.println("Number of attributes in model = "
                + attrSampleNum);
        System.out.println("Number of samples = " + sampleNum);
        System.out.println("Summary: " + summary);


        // a classifier for decision trees:
        J48 j48 = new J48();

        //Some preprocessing is carried out on the data in the java program
        //filter for converting numerical attributes to nominal (J48 trees cannot handle numeric class as target attributes)
        //The attributes: remorse, religion, denial, anger & acceptance are onverted
        NumericToNominal n = new NumericToNominal();
        n.setAttributeIndices("21,22,23,24,25,26");

        // filter for removing samples:
        Remove rm = new Remove();
        rm.setAttributeIndices("1,2,3,4,5,7,9,10,11,13,15,16,17,20,23,24,25,26"); // remove irrelevant attributes

        // filtered classifier
        FilteredClassifier fc = new FilteredClassifier();
        fc.setFilter(rm);
        fc.setFilter(n);
        fc.setClassifier(j48);



        // Create counters and print values
        float correct = 0;
        float incorrect = 0;

        // train using stock_training_data.arff:
        fc.buildClassifier(training_data);


        System.out.println(testing_data.classAttribute().value((int) testing_data.instance(2).classValue()));
        // test using stock_testing_data.arff:
        for (int i = 0; i < testing_data.numInstances(); i++) {
            double pred = fc.classifyInstance(testing_data.instance(i));
            System.out.print("Expected values: "
                    + testing_data.classAttribute().value(
                    (int) testing_data.instance(i).classValue()));
            System.out.println(", Predicted values: "
                    + testing_data.classAttribute().value((int) pred));
            // Increment correct/incorrect values
            if (testing_data.classAttribute().value(
                    (int) testing_data.instance(i).classValue()) == testing_data.classAttribute().value((int) pred)) {
                correct += 1;
            } else {
                incorrect += 1;
            }
        }

        //Print correct/incorrect
        float perCorrect = correct/(correct+incorrect)*100;
        System.out.println("Number correct: " + correct + "\nNumber incorrect: " + incorrect + "\nPercent correct: " +
                perCorrect + "%");

        final javax.swing.JFrame jf =
                new javax.swing.JFrame("Weka Classifier Tree Visualizer: J48");
        jf.setSize(500,400);
        jf.getContentPane().setLayout(new BorderLayout());
        TreeVisualizer tv = new TreeVisualizer(null,
                j48.graph(),
                new PlaceNode2());
        jf.getContentPane().add(tv, BorderLayout.CENTER);
        jf.addWindowListener(new java.awt.event.WindowAdapter() {
            public void windowClosing(java.awt.event.WindowEvent e) {
                jf.dispose();
            }
        });

        jf.setVisible(true);
        tv.fitToScreen();

    }

}
