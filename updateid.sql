DELIMITER //
drop procedure up_she_id//
create procedure up_she_id()
begin
declare done int default 0;
declare curid varchar(255);
declare idx int default 1000;
declare cs cursor for select shelter_id from Shelter;
declare continue handler for not FOUND set done = 1;

open cs;
repeat 
    fetch cs into curid;
    
	repeat
		set idx = idx+1;
		set @newid = LTRIM(idx);
	until (not @newid in (select shelter_id from Shelter))
    end repeat;
    
    update Shelter
	set shelter_id = @newid
	where shelter_id = curid;
    
UNTIL done
end repeat;
close cs;
end//
DELIMITER ;