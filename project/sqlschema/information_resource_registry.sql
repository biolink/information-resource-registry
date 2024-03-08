-- # Class: "NamedThing" Description: "A generic grouping for any identifiable entity"
--     * Slot: id Description: A unique identifier for a thing
--     * Slot: name Description: A human-readable name for a thing
--     * Slot: description Description: A human-readable description for a thing
-- # Class: "InformationResourceContainer" Description: "Represents a InformationResourceContainer"
--     * Slot: primary_email Description: The main email address of a person
--     * Slot: birth_date Description: Date on which a person is born
--     * Slot: age_in_years Description: Number of years since birth
--     * Slot: vital_status Description: living or dead status
--     * Slot: id Description: A unique identifier for a thing
--     * Slot: name Description: A human-readable name for a thing
--     * Slot: description Description: A human-readable description for a thing
--     * Slot: InformationResourceContainerCollection_id Description: Autocreated FK slot
-- # Class: "InformationResourceContainerCollection" Description: "A holder for InformationResourceContainer objects"
--     * Slot: id Description: 

CREATE TABLE "NamedThing" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE "InformationResourceContainerCollection" (
	id INTEGER NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE "InformationResourceContainer" (
	primary_email TEXT, 
	birth_date DATE, 
	age_in_years INTEGER, 
	vital_status VARCHAR(7), 
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	"InformationResourceContainerCollection_id" INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY("InformationResourceContainerCollection_id") REFERENCES "InformationResourceContainerCollection" (id)
);