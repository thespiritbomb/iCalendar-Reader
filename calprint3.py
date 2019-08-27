/*
 * calprint4.c
 *
 * Starter file provided to students for Assignment #4, SENG 265,
 * Summer 2019.
 */
#include <time.h>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "emalloc.h"
#include "ics.h"
#include "listy.h"
#define BUFLEN 100
//A user defined function to check whether a given string starts with a given prefix
_Bool starts_with(const char *string, const char *prefix)
{
    while(*prefix)
    {
        if(*prefix++ != *string++)
            return 0;
    }

    return 1;
}
//A user defined function to copy values from the Original Linked List to the Major Linked List
node_t *copyValuesToMajorLL(node_t *n, node_t *headMajor){
	assert(n!=NULL);
	node_t *temp_node=NULL;
	event_t *temp_event=NULL;
	while(n->val!=NULL){
		temp_event=emalloc(sizeof(event_t));
		strncpy(temp_event->dtstart,n->val->dtstart,17);
		strncpy(temp_event->dtend,n->val->dtend,17);
		strncpy(temp_event->location,n->val->location,LOCATION_LEN);
		strncpy(temp_event->summary,n->val->summary,SUMMARY_LEN);
		strncpy(temp_event->rrule,n->val->rrule,RRULE_LEN);
		if (headMajor==NULL){
			headMajor=new_node(temp_event);
		}
		else{
			temp_node=new_node(temp_event);
			headMajor=add_front(headMajor,temp_node);
		}
		if(n->next==NULL)
			break;
		n=n->next;
	}
	return headMajor;
}
//A user defined function to create struct tm variables from event details
void create_time_t(struct tm *eventtm,event_t *event){
	char tempstr4[4],tempstr2[2];
	int tempvar;
	strncpy(tempstr4,event->dtstart,4);
	tempvar=atoi(tempstr4);
	eventtm->tm_year = (tempvar-1900);
	strncpy(tempstr2,(event->dtstart)+4, 2);
	eventtm->tm_mon = atoi(tempstr2)-1;
	strncpy(tempstr2,(event->dtstart)+6, 2);
	eventtm->tm_mday = atoi(tempstr2);
	strncpy(tempstr2,(event->dtstart)+9, 2);
	eventtm->tm_hour = atoi(tempstr2); 
	strncpy(tempstr2,(event->dtstart)+11, 2);
	eventtm->tm_min = atoi(tempstr2); 
	strncpy(tempstr2,(event->dtstart)+13, 2);
	eventtm->tm_sec = atoi(tempstr2);
}
//A user defined function to create the Major Linked List
node_t *createMajorLL(node_t *n){
	assert(n!=NULL);
	node_t *headMajor=NULL;
	//Copying all values from original LL to Major LL
	headMajor=copyValuesToMajorLL(n,headMajor);
	event_t *event=NULL;
	event_t *temp_event=NULL;
	node_t *temp_node=NULL;
	char temprruleuntil[15];
	char tempstr4[4],tempdatestr[15],tempstr2[2]; //tempstr4 for filling struct tm year //tempdatestr for filling dtstart on new event //tempstr2 for filling struct tm day,month,hr,min,sec
	struct tm eventStartDT={0};
	struct tm eventEndDT={0};
	struct tm eventRRuleUntil={0};
	struct tm tempDT={0};
	int tempvar;
	while(n!=NULL){
		event = n->val;
		if (strcmp(event->rrule, "") != 0) {
	    	//EXTRACTING start date and time of an event
	    	create_time_t(&eventStartDT,event);
			//EXTRACTING end date and time of an event
			create_time_t(&eventEndDT,event);
		    //Getting the until date from rrule of the event
		    strncpy(temprruleuntil, (event->rrule)+26, 15);
		    //EXTRACTING details of the rrule until date
		    strncpy(tempstr4,temprruleuntil, 4);
		    tempvar=atoi(tempstr4);
			eventRRuleUntil.tm_year = (tempvar-1900);
			strncpy(tempstr2,temprruleuntil+4, 2);
			eventRRuleUntil.tm_mon = atoi(tempstr2)-1;
			strncpy(tempstr2,temprruleuntil+6, 2);
			eventRRuleUntil.tm_mday = atoi(tempstr2);
			strncpy(tempstr2,temprruleuntil+9, 2);
			eventRRuleUntil.tm_hour = atoi(tempstr2); 
			strncpy(tempstr2,temprruleuntil+11, 2);
			eventRRuleUntil.tm_min = atoi(tempstr2);
			strncpy(tempstr2,temprruleuntil+13, 2);
			eventRRuleUntil.tm_sec = atoi(tempstr2);
			//Increment once before entering the loop
			eventStartDT.tm_mday+=7;
			mktime(&eventStartDT);
			eventEndDT.tm_mday+=7;
			mktime(&eventEndDT);
		    while(difftime(mktime(&eventRRuleUntil),mktime(&eventStartDT))>0){
		    	temp_event = emalloc(sizeof(event_t));
				temp_event->rrule[0] = '\0';
				tempDT.tm_year=eventStartDT.tm_year;
				tempDT.tm_mon=eventStartDT.tm_mon;
				tempDT.tm_mday=eventStartDT.tm_mday;
				tempDT.tm_hour=eventStartDT.tm_hour;
				tempDT.tm_min=eventStartDT.tm_min;
				tempDT.tm_sec=eventStartDT.tm_sec;
				strftime(tempdatestr,17,"%Y%m%dT%H%M%S",&tempDT);
				strncpy(temp_event->dtstart, tempdatestr, 17);
				tempDT.tm_year=eventEndDT.tm_year;
				tempDT.tm_mon=eventEndDT.tm_mon;
				tempDT.tm_mday=eventEndDT.tm_mday;
				tempDT.tm_hour=eventEndDT.tm_hour;
				tempDT.tm_min=eventEndDT.tm_min;
				tempDT.tm_sec=eventEndDT.tm_sec;
				strftime(tempdatestr,17,"%Y%m%dT%H%M%S",&tempDT);
				strncpy(temp_event->dtend, tempdatestr, 17);
				strncpy(temp_event->location, event->location, LOCATION_LEN);
				strncpy(temp_event->summary, event->summary, SUMMARY_LEN);
				if (headMajor==NULL)
					headMajor=new_node(temp_event);
				else{
					temp_node = new_node(temp_event);
    				headMajor = add_front(headMajor, temp_node);
    			}
				eventStartDT.tm_mday+=7;
				mktime(&eventStartDT);
				eventEndDT.tm_mday+=7;
				mktime(&eventEndDT);
			}		    
	    } 
	    n=n->next;
	}
	return headMajor;
}
//A user defined function to create the original Linked List
node_t *createEventsLL(char *filename){
	FILE *ics;
	char buffer[BUFLEN];
	event_t *temp_event = NULL;
    node_t  *temp_node  = NULL;
    node_t  *head = NULL;
	ics=fopen(filename,"r");
	
	if(ics==NULL){
		printf("File not found");
		exit(0);
	}
	
	while (fgets(buffer, sizeof(char) * BUFLEN, ics)) {
		if(strncmp(buffer,"BEGIN:VEVENT",11)==0){
			temp_event = emalloc(sizeof(event_t));
			temp_event->rrule[0] = '\0';
		}
		else if(strncmp(buffer,"END:VEVENT",9)==0){
			if(head!=NULL){
				temp_node = new_node(temp_event);
    			head = add_front(head, temp_node);
    		}
    		else{
    			head=new_node(temp_event);
    		}
		}
		//Getting the Start Date and Time of the event
		else if(starts_with(buffer,"DTSTART:")){
			buffer[strcspn(buffer, "\n")] = '\0';
			strncpy(temp_event->dtstart,buffer+8, 17);
		}
		//Getting the End Date and Time of the event
		else if(starts_with(buffer,"DTEND:")){
			buffer[strcspn(buffer, "\n")] = '\0';
			strncpy(temp_event->dtend,buffer+6, 17);
		}
		//Getting the RRULE of the event
		else if(starts_with(buffer,"RRULE:")){
			buffer[strcspn(buffer, "\n")] = '\0';
			strncpy(temp_event->rrule, buffer+6, RRULE_LEN);
		}  
		//Getting the Location of the event
		else if(starts_with(buffer,"LOCATION:")){
			buffer[strcspn(buffer, "\n")] = '\0';
			strncpy(temp_event->location, buffer+9, LOCATION_LEN);
		}
		//Getting the Summary of the event
		else if(starts_with(buffer,"SUMMARY:")){
			buffer[strcspn(buffer, "\n")] = '\0';
			strncpy(temp_event->summary, buffer+8, SUMMARY_LEN);
		}
	}
	fclose(ics);
	return head;
}

int main(int argc, char *argv[])
{
	node_t *LLStart,*majorLLStart,*n;
	struct tm inputStartDTtm={0};
	struct tm inputEndDTtm={0};
	struct tm eventTM={0};
	struct tm eventTM2={0};
	char inputStartDT[17],inputEndDT[17],tempOutputStr[100];
    int from_y = 0, from_m = 0, from_d = 0;
    int to_y = 0, to_m = 0, to_d = 0;
    char *filename = NULL;
    int i; 
    event_t *event;
    for (i = 0; i < argc; i++) {
        if (strncmp(argv[i], "--start=", 7) == 0) {
            sscanf(argv[i], "--start=%d/%d/%d", &from_d, &from_m, &from_y);
        } 
		else if (strncmp(argv[i], "--end=", 5) == 0) {
            sscanf(argv[i], "--end=%d/%d/%d", &to_d, &to_m, &to_y);
        } 
		else if (strncmp(argv[i], "--file=", 7) == 0) {
            filename = argv[i]+7;
        }
    }
    if (from_y == 0 || to_y == 0 || filename == NULL) {
        fprintf(stderr, 
            "usage: %s --start=dd/mm/yyyy --end=dd/mm/yyyy --file=icsfile\n",
            argv[0]);
        exit(1);
    }
//    creating Linked List of the original events
    LLStart=createEventsLL(filename);
//    creating a major Linked List with original + repeated events
    majorLLStart=createMajorLL(LLStart);
//	creating strings in the format YYYYMMDDTHHMMSS
    sprintf(inputStartDT,"%d%02d%02dT000000",from_y,from_m,from_d);
    sprintf(inputEndDT,"%d%02d%02dT235959",to_y,to_m,to_d);
//	creating a date format for comparisons and clarity
    inputStartDTtm.tm_year = (from_y-1900);
    inputStartDTtm.tm_mon = (from_m-1);
    inputStartDTtm.tm_mday = from_d;
    inputStartDTtm.tm_hour = 0;
    inputStartDTtm.tm_min = 0;
    inputStartDTtm.tm_sec = 0;
    inputEndDTtm.tm_year = (to_y-1900);
    inputEndDTtm.tm_mon = (to_m-1);
    inputEndDTtm.tm_mday = to_d;
    inputEndDTtm.tm_sec = 59;
	inputEndDTtm.tm_min = 59;
    inputEndDTtm.tm_hour = 23;
    mktime(&inputStartDTtm);
    mktime(&inputEndDTtm);
    bool firstDate=1;
    //Printing Final Output
    while(difftime(mktime(&inputEndDTtm),mktime(&inputStartDTtm))>0){
    	n=majorLLStart;
    	bool firstevt=1;
    	while(n!=NULL){
    		event=n->val;
    		if((strncmp(event->dtstart,inputStartDT,4)==0)&&(strncmp((event->dtstart)+4,inputStartDT+4,2)==0)&&(strncmp((event->dtstart)+6,inputStartDT+6,2)==0)){
    			if(!firstDate)
    			printf("\n");
    			if(firstevt){
    				strftime(tempOutputStr,sizeof(tempOutputStr),"%B %d, %Y (%a)\n",&inputStartDTtm);
    				if(!firstDate)
    				printf("\n%s",tempOutputStr);
    				else
    				printf("%s",tempOutputStr);
    				firstDate=0;
    				int len = strlen(tempOutputStr)-2;
    				for(int i=0;i<=len;i++)
    				printf("-");
    				printf("\n");
    				firstevt=0;
				}
				create_time_t(&eventTM,event);
				mktime(&eventTM);
				create_time_t(&eventTM2,event);
				mktime(&eventTM2);
				strftime(tempOutputStr,sizeof(tempOutputStr),"%I:%M %p to ",&eventTM);
				if(starts_with(tempOutputStr,"0")){
					strncpy(tempOutputStr," ",1);
				}
				printf("%s",strlwr(tempOutputStr));
				strftime(tempOutputStr,sizeof(tempOutputStr),"%I:%M %p: ",&eventTM2);
				if(starts_with(tempOutputStr,"0")){
					strncpy(tempOutputStr," ",1);
				}
				printf("%s",strlwr(tempOutputStr));
				printf("%s [%s]",event->summary,event->location);
			}
			n=n->next;
		}
    	inputStartDTtm.tm_mday+=1;
    	mktime(&inputStartDTtm);
    	sprintf(inputStartDT,"%d%02d%02dT235959",inputStartDTtm.tm_year+1900,inputStartDTtm.tm_mon+1,inputStartDTtm.tm_mday);
	}	
    exit(0);
}