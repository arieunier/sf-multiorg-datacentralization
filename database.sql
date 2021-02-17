drop schema consolidated CASCADE;
create schema consolidated;
create table consolidated.opportunities(
        sfopportunityid varchar(255) not null primary key,
        sfaccountid varchar(255) not null, 
        opportunityname varchar(255) not null,
        opportunityamount varchar(255) not null,
        opportunitystage varchar(255) not null, 
        opportunityfiscalyear varchar(255) not null, 
        opportunityfiscalquarter varchar(255) not null);

    