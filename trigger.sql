DELIMITER //
/*
drop trigger pet_tri//
drop trigger pet_aft//
drop trigger she_tri//
drop trigger usp_tri//
*/
create trigger pet_tri
before insert on Pet 
for each row
begin
insert ignore into Preference(pet_type, age, color) 
	values (new.pet_type, new.intake_age+2021-year(new.intake_time), new.color);
insert ignore into Shelter(shelter_id, shelter_status, location)
	values (new.shelter_id, 'open', new.shelter_id);
if (new.UID is not null) then
insert ignore into Users(UID)
	values (new.UID);
insert ignore into Favors(UID, pet_id)
	values (new.UID, new.pet_id);
end if;
end//

create trigger pet_aft
after insert on Pet 
for each row
begin
if (new.UID is not null) then
	insert ignore into Users(UID)
		values (new.UID);
	insert ignore into Favors(UID, pet_id)
		values (new.UID, new.pet_id);
	insert ignore into User_preference(UID, pet_type, age, color)
		values (new.UID, new.pet_type, new.intake_age+2021-year(new.intake_time), new.color);
	if(new.shelter_id is not null) then
		update Users set location = (select location from Shelter where shelter_id=new.shelter_id) where UID=new.UID;
	end if;
end if;
end//

create trigger she_tri
before insert on Shelter
for each row
begin
insert ignore into Address(location, state)
	values (new.location, 'TX');
end//

create trigger usp_tri
before insert on User_preference
for each row
begin
insert ignore into Users(UID)
	values (new.UID);
insert ignore into Preference(pet_type, age, color) 
	values (new.pet_type, new.age, new.color);
end//

DELIMITER ;