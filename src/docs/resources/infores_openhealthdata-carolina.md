[//]: # (DO NOT MANUALLY EDIT THIS FILE. IT IS GENERATED FROM A TEMPLATE.)

## Open Health Data @ Carolina (infores:openhealthdata-carolina)

**Status**: released
  
**Knowledge Level**: statistical_association
  
**Agent Type**: not_provided

**Description**: Open Health Data @ Carolina provides access to counts and frequencies (i.e., EHR prevalence) of conditions, procedures, drug exposures, and patient demographics, and the co-occurrence frequencies between them. Count and frequency data were derived from UNC Health's OMOP database on a five-year cohort (~6M patients over years 2018 through 2022) of all UNC Health patients,  including their inpatient and outpatient visit data. Counts represent the number of  patients associated with a given concept, e.g., diagnosed with a condition,  exposed to a drug, or who had a procedure. Frequencies are the number of unique patients associated with the concept divided by the total number of patients in the dataset,  i.e., prevalence in the electronic health records. To protect patient privacy,  all concepts and pairs of concepts where the count was <= 10 were excluded,  and counts were randomized by the Poisson distribution.**Synonyms**:

- OHD@Carolina, Open Health Data @ Carolina

**Cross References**:

- [https://github.com/NCATSTranslator/Translator-All/wiki/Open-Health-Data-at-Carolina](https://github.com/NCATSTranslator/Translator-All/wiki/Open-Health-Data-at-Carolina)


**Consumed by**:

- infores:automat-openhealthdata-carolina