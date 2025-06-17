[//]: # (DO NOT MANUALLY EDIT THIS FILE. IT IS GENERATED FROM A TEMPLATE.)

## Columbia Open Health Data (COHD) (infores:cohd)

**Status**: released
  
**Knowledge Level**: statistical_association
  
**Agent Type**: not_provided

**Description**: The Columbia Open Health Data (COHD) API provides access to counts and frequencies (i.e., EHR prevalence) of conditions, procedures, drug exposures, and patient demographics, and the co-occurrence frequencies between them. Count and frequency data were derived from the [Columbia University Medical Center''s](http://www.cumc.columbia.edu/) [OHDSI](https://www.ohdsi.org/) database including inpatient and outpatient data. Counts are the number of patients associated with the concept, e.g., diagnosed with a condition, exposed to a drug, or who had a procedure. Frequencies are the number of unique patients associated with the concept divided by the total number of patients in the dataset, i.e., prevalence in the electronic health records. To protect patient privacy, all concepts and pairs of concepts where the count <= 10 were excluded, and counts were randomized by the Poisson distribution.           Four datasets are available:  1) 5-year non-hierarchical dataset: Includes clinical data from 2013-2017   2) lifetime non-hierarchical dataset: Includes clinical data from all dates   3) 5-year hierarchical dataset: Counts for each concept include patients from descendant concepts. Includes clinical data from 2013-2017. 4) BETA! Temporal co-occurrence data  In the 5-year hierarchical data set, the counts for each concept include the patients from all descendant concepts. For example, the count for ibuprofen (ID 1177480) includes patients with Ibuprofen 600 MG Oral Tablet (ID 19019073 patients), Ibuprofen 400 MG Oral Tablet (ID 19019072), Ibuprofen 20 MG/ML Oral Suspension (ID 19019050), etc.   While the lifetime dataset captures a larger patient population and range of concepts, the 5-year dataset has better underlying data consistency.   Clinical concepts (e.g., conditions, procedures, drugs) are coded by their standard concept ID in the [OMOP Common Data Model](https://github.com/OHDSI/CommonDataModel/wiki). API methods are provided to map to/from other vocabularies supported in OMOP and other ontologies using the EMBL-EBI Ontology Xref Service (OxO).    The following resources are available through this API:    1. Metadata: Metadata on the COHD database, including dataset descriptions, number of concepts, etc.    2. OMOP: Access to the common vocabulary for name and concept identifier mapping   3. Clinical Frequencies: Access to the counts and frequencies of conditions, procedures, and drug exposures, and the associations between them. Frequency was determined as the number of patients with the code(s) / total number of patients.    4. Concept Associations: Inferred associations between concepts using chi-square analysis, ratio between observed to expected frequency, and relative frequency.    A [Python notebook](https://github.com/WengLab-InformaticsResearch/cohd_api/blob/master/notebooks/COHD_API_Example.ipynb) demonstrates simple examples of how to use the COHD API.   COHD was developed at the [Columbia University Department of Biomedical Informatics](https://www.dbmi.columbia.edu/) as a collaboration between the [Weng Lab](http://people.dbmi.columbia.edu/~chw7007/), [Tatonetti Lab](http://tatonettilab.org/), and the [NCATS Biomedical Data Translator](https://ncats.nih.gov/translator) program (Red Team). This work was supported in part by grants: NCATS OT3TR002027, NLM R01LM009886-08A1, and NIGMS R01GM107145.  The following external resources may be useful:   [OHDSI](https://www.ohdsi.org/)   [OMOP Common Data Model](https://github.com/OHDSI/CommonDataModel/wiki)   [Athena](http://athena.ohdsi.org) (OMOP vocabularies, search, concept relationships, concept hierarchy)   [Atlas](http://www.ohdsi.org/web/atlas/) (OMOP vocabularies, search, concept relationships, concept hierarchy, concept sets)

**Cross References**:

- [https://github.com/NCATSTranslator/Translator-All/wiki/COHD-KP](https://github.com/NCATSTranslator/Translator-All/wiki/COHD-KP)


**Consumed by**:

- infores:aragorn
- infores:arax
- infores:openpredict
- infores:service-provider-trapi