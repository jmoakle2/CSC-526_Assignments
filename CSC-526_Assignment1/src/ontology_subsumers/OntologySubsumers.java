/*
 * Justin Oakley
 * CSC 526 Assignment 1: Ontology Subsumers
 * 02/06/19
 */
package ontology_subsumers;

// Load necessary imports to the java file.
import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.Scanner;
import java.util.Set;

import org.junit.Test;
import org.semanticweb.elk.owlapi.ElkReasonerConfiguration;
import org.semanticweb.elk.owlapi.ElkReasonerFactory;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.IRI;
import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLDataFactory;
import org.semanticweb.owlapi.model.OWLException;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyManager;
import org.semanticweb.owlapi.reasoner.ConsoleProgressMonitor;
import org.semanticweb.owlapi.reasoner.InferenceType;
import org.semanticweb.owlapi.reasoner.NodeSet;
import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.OWLReasonerConfiguration;
import org.semanticweb.owlapi.reasoner.OWLReasonerFactory;

public class OntologySubsumers {
	
	
	/*
	 * This method is used to load a text file containing the given GO identifiers, find the superclasses
	 * of said identifiers using the "go.owl" file, and then print the original identifier and their
	 * superclass identifiers into a TSV file.
	 */
	@Test
	public static void PrintSuperclasses() throws OWLException, FileNotFoundException {
		
		/*
		 * Load "go.owl" file from "http://purl.obolibrary.org/obo/go.owl" into an OWLOntology. Then, output
		 * what ontology was loaded.
		 */
		String DOCUMENT_IRI = "http://purl.obolibrary.org/obo/go.owl";
		OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
		IRI docIRI = IRI.create(DOCUMENT_IRI);
		OWLOntology ont = manager.loadOntologyFromOntologyDocument(docIRI);
		
		System.out.println("Loaded " + ont.getOntologyID() + "\n");
		
		/*
		 * Utilize the Elk-Reasoner for ontology processing, then precompute inferences. 
		 */
		OWLReasonerFactory reasonerFactory = new ElkReasonerFactory();
		ConsoleProgressMonitor progressMonitor = new ConsoleProgressMonitor();
		OWLReasonerConfiguration config = new ElkReasonerConfiguration(progressMonitor);
		OWLReasoner reasoner = reasonerFactory.createReasoner(ont, config);
		
		System.out.println();
		reasoner.precomputeInferences(InferenceType.CLASS_HIERARCHY);
		
		/*
		 * Create the OWLDataFactory and load the file (which is called "ontology_ids.txt")
		 * that contains all the given GO IDs and create the PrintWriter that will create
		 * the TSV file needed for output (which will be called "ontology_ids_superclasses.tsv").
		 * 
		 * The given GO IDs are:
		 * 			{ GO_0003677, GO_0003700, GO_0005634, GO_0006355, GO_0006986, GO_0016020, GO_0016021,
		 * 			  GO_0043565, GO_0045449, GO_0046983 }
		 */
		OWLDataFactory fac = manager.getOWLDataFactory();
		File file = new File("ontology_ids.txt");
		Scanner scan = new Scanner(file);
		PrintWriter output = new PrintWriter("ontology_ids_superclasses.tsv");
		
		/*
		 * Run a while loop to iterate through the GO IDs file, find the OWLClass in the ontology
		 * that corresponds with the current identifier, obtain its superclasses and then add
		 * them to a String in a comma separated list format. Once the identifier and its superclasses
		 * have been appropriately found in the ontology and formatted, write them to the TSV file.
		 */
		while(scan.hasNext()){
			String line = scan.next();
			OWLClass go = fac.getOWLClass(IRI.create("http://purl.obolibrary.org/obo/" + line));
			NodeSet<OWLClass> superClses = reasoner.getSuperClasses(go, false);
			Set<OWLClass> clses = superClses.getFlattened();
			String superClsOutput = "";
			boolean firstCls = false;
			
			for (OWLClass cls : clses) {
				if(!cls.getIRI().getShortForm().equals("Thing")){
					if(firstCls){
						superClsOutput = superClsOutput + ",";
					}

					superClsOutput = superClsOutput + cls.getIRI().getShortForm();
					firstCls = true;
				}
	        }
			
			output.println(line + "\t" + superClsOutput);
		}
		
		/*
		 * Close the PrintWriter object and the Scanner used for reading the file.
		 */
		output.close();
		scan.close();
	}
	
	/*
	 * Main method used to run the PrintSuperclasses method.
	 */
	public static void main(String[] args) throws OWLException, FileNotFoundException{
		PrintSuperclasses();
	}
}
