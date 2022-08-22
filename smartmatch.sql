DELIMITER //
drop procedure smartMatch//
create procedure smartMatch(
	in do_fav int,
    in matcher_uid int
    )
begin

declare cs_kind cursor for select distinct pet_type, color from Preference;
declare cs_pet cursor for select pet_id from Pet;

DROP TABLE IF EXISTS `FinalTable`;
create table FinalTable (
	pet_type VARCHAR(255),
	color VARCHAR(255),
	like_num int,
	heal_num int,
    rate VARCHAR(255),
    PRIMARY KEY(pet_type, color));

insert into FinalTable (pet_type, color, like_num, heal_num)
    (select pet_type, color, like_num, heal_num
    from ((select pet_type, color, count(distinct UID) as like_num 
		from Preference natural join User_preference  
        group by pet_type, color) as u 
	natural join (select pet_type, color, count(distinct pet_id) as heal_num 
		from Pet 
        where pet_condition = 'Normal' 
        group by pet_type, color) as p));
        

begin
declare done int default 0;
declare cur_type VARCHAR(255);
declare cur_color VARCHAR(255);
declare continue handler for not found set done = 1;

open cs_kind;

repeat
	fetch cs_kind into cur_type, cur_color;
    set @un = (select like_num from FinalTable where pet_type=cur_type and color=cur_color);
    set @hn = (select heal_num from FinalTable where pet_type=cur_type and color=cur_color);

    if @un/@hn <= 0.5 then 
        update FinalTable
        set rate = 'Plenty of pets, you can wait.'
        where pet_type=cur_type and color=cur_color;
    end if;
    if @un/@hn <= 0.6 and @un/@hn > 0.5 then 
        update FinalTable
        set rate = 'Enough pets, you can wait.'
        where pet_type=cur_type and color=cur_color;
    end if;
	if @un/@hn <= 0.7 and @un/@hn > 0.6 then 
        update FinalTable
        set rate = 'Balanced supply & demand.'
        where pet_type=cur_type and color=cur_color;
    end if;
	if @un/@hn <= 0.8 and @un/@hn > 0.7 then 
        update FinalTable
        set rate = 'Hot type, decide fast.'
        where pet_type=cur_type and color=cur_color;
    end if;
    if @un/@hn <= 1 and @un/@hn > 0.8 then 
        update FinalTable
        set rate = 'Very hot type, decide fast!'
        where pet_type=cur_type and color=cur_color;
    end if;
    if @un/@hn <= 1.2 and @un/@hn > 1 then 
        update FinalTable
        set rate = 'Star type, act fast!'
        where pet_type=cur_type and color=cur_color;
    end if;
    if @un/@hn <= 1.5 and @un/@hn > 1.2 then 
        update FinalTable
        set rate = 'Hot star type, act now!'
        where pet_type=cur_type and color=cur_color;
    end if;
    if @un/@hn > 1.5 then 
        update FinalTable
        set rate = 'Almost gone, adopt immediatly!'
        where pet_type=cur_type and color=cur_color;
    end if;
    
until done end repeat;
close cs_kind;
end;


if do_fav=1 then
	begin
	declare done int default 0;
	declare cur_id int;
	declare continue handler for not found set done = 1;
	open cs_pet;
    
    repeat
		fetch cs_pet into cur_id;
        if exists(select pet_type, color from 
					(select pet_id, pet_type, color from Pet where pet_id=cur_id) as pt 
                    natural join (select * 
								from Preference natural join User_preference 
                                where UID=matcher_uid) as ut) then
                    
			delete from Favors where UID=matcher_uid and pet_id=cur_id;
            insert into Favors values (matcher_uid, cur_id);
            
		end if;
	until done end repeat;
    close cs_pet;
    end;
end if;

select *
from FinalTable
where (pet_type,color) in ((select pet_type, color 
						from Preference natural join User_preference 
                        where UID=matcher_uid)
                        union 
                        (select p.pet_type as pet_type, p.color as color 
                        from Favors as f join Pet as p on f.pet_id=p.pet_id
                        where f.UID=matcher_uid))
order by like_num desc;

end//

DELIMITER ;