"""
Returns the criteria_profile_id id errors in the criteria_profile_table
"""

from database_mysql_local.generic_crud import GenericCRUD
import pandas as pd


# TO DO: Implement age checking as the code just returns true for all age queries
# as long as they have values present
class phase_1:


    def get_data(self, limit_num: int = 1000) -> list:
        """
        Returns the criteria_profile_id id errors in the criteria_profile_table

        """
        gencrud = GenericCRUD(default_schema_name="profile")

        query = """
        SELECT
            criteria_profile_table.criteria_profile_id as criteria_profile_id, 
            criteria_profile_table.criteria_id AS `query.criteria_id`,
            criteria_profile_table.profile_id AS `query.profile_id`,
            criteria_table.name AS `criteria.name`,
            people_criteria_table.min_age AS `criteria.min_age`,
            people_criteria_table.max_age AS `criteria.max_age`,
            people_criteria_table.gender_list_id AS `criteria.gender_list_id`,
            criteria_table.location_id AS `criteria.location_id`,
            location_criteria_table.location_id_old AS `criteria.location_criteria_id`,
            location_criteria_table.location_type_id AS `criteria.location_type_id`,
            criteria_table.label_id AS `criteria.label_id`,
            criteria_table.country_id_old AS `criteria.country_id`,
            criteria_location.name AS `criteria.country_name`,
            criteria_table.group_id AS `criteria.group_id`,
            criteria_table.group_list_id AS `criteria.group_list_id`,
            criteria_table.location_list_id AS `criteria.location_list_id`,
            location_criteria_table.city_list_id AS `criteria.city_list_id`,
            location_criteria_table.location_type_id AS `criteria_location.location_type_id`,
            profile_table.profile_id AS `profile.profile_id`,
            profile_table.is_main,
            gender_table.gender_id AS `profile.gender_id`,
            gender_table.name AS `profile.gender`,
            gender_list_member_table.gender_list_id AS `profile.gender_list_id`,
            person_table.birthday_date AS `person.birthday_date`,
            location_table.location_id AS `profile.location_id`,
            country_table.name AS `profile.country_name`,
            country_table.country_id AS `profile.country_id`,
            city_list_member_table.city_list_id AS `profile.city_list_id`,
            group_profile_table.group_id AS `profile.group_id`,
            group_list_table.group_list_id AS `profile.group_list_id`,
            group_list_table.name AS `profile.group_list_name`,
            group_country.name AS `profile.group_country`,
            location_list_table.location_list_id AS `profile.location_list_id`,
            location_type_ml_table.title AS `profile.location_type`,
            location_type_ml_table.location_type_id AS `profile.location_type_id`
        FROM
            criteria_profile.criteria_profile_table
            LEFT JOIN criteria.criteria_table ON criteria_profile_table.criteria_id = criteria_table.criteria_id
            LEFT JOIN location.location_criteria_table ON criteria_profile_table.criteria_id = location_criteria_table.criteria_id
            LEFT JOIN location.city_list_table ON location_criteria_table.city_list_id = city_list_table.city_list_id
            LEFT JOIN people.people_criteria_table ON people_criteria_table.criteria_id = criteria_profile_table.criteria_id
            LEFT JOIN profile.profile_table ON profile_table.profile_id = criteria_profile_table.profile_id
            LEFT JOIN gender.gender_table ON profile_table.`profile.gender_id` = gender_table.gender_id
            LEFT JOIN gender.gender_list_member_table ON profile_table.`profile.gender_id` = gender_list_member_table.gender_id
            LEFT JOIN person.person_table ON profile_table.main_person_id = person_table.person_id
            LEFT JOIN location_profile.location_profile_table ON profile_table.profile_id = location_profile_table.profile_id
            LEFT JOIN location.location_table ON location_profile_table.location_id = location_table.location_id
            LEFT JOIN location.country_table ON location_table.country_id = country_table.country_id
            LEFT JOIN location.country_table AS criteria_location ON criteria_table.country_id_old = criteria_location.country_id
            LEFT JOIN location.city_list_member_table ON location_table.city_id = city_list_member_table.city_id
            LEFT JOIN group_profile.group_profile_table ON group_profile_table.profile_id = criteria_profile_table.profile_id
            LEFT JOIN group_location.group_location_table ON group_profile_table.group_id = group_location_table.group_id
            LEFT JOIN location.location_table AS location2 ON group_location_table.location_id = location2.location_id
            LEFT JOIN location.country_table AS group_country ON location2.country_id = group_country.country_id
            LEFT JOIN `group`.group_table ON group_table.group_id = group_profile_table.group_id
            LEFT JOIN `group`.group_list_member_table ON group_table.group_id = group_list_member_table.group_id
            LEFT JOIN `group`.group_list_table ON group_list_member_table.group_list_id = group_list_table.group_list_id
            LEFT JOIN location.location_list_member_table ON location_table.location_id = location_list_member_table.location_id
            LEFT JOIN location.location_list_table ON location_list_table.location_list_id 
            = location_list_member_table.location_list_id
            LEFT JOIN location_location_type.location_location_type_table ON location_location_type_table.location_id
            = location_table.location_id
            LEFT JOIN location.location_type_ml_table ON location_type_ml_table.location_type_id = location_location_type_table.location_type_id
            LEFT JOIN label_location.label_location_table ON location_table.location_id = label_location_table.location_id
        WHERE
            (
                people_criteria_table.gender_list_id IS NOT NULL
                AND EXISTS (
                    SELECT 1
                    FROM people.people_criteria_table
                    WHERE gender_list_member_table.gender_list_id = people_criteria_table.gender_list_id
                )
                AND gender_list_member_table.gender_list_id = people_criteria_table.gender_list_id
            )
            OR (
                people_criteria_table.min_age IS NOT NULL
                OR people_criteria_table.max_age IS NOT NULL
            )
            OR (
                criteria_table.country_id_old IS NOT NULL
                AND country_table.country_id IS NOT NULL
                AND (
                    location_criteria_table.location_id_old IS NULL
                    OR location_criteria_table.location_type_id IS NULL
                )
                AND EXISTS (
                    SELECT 1
                    FROM criteria.criteria_table
                    WHERE country_table.country_id = criteria_table.country_id_old
                )
                AND country_table.country_id = criteria_table.country_id_old
            )
            OR (
                location_criteria_table.city_list_id IS NOT NULL
                AND location_criteria_table.location_type_id IS NOT NULL
                AND EXISTS (
                    SELECT 1
                    FROM location.location_criteria_table
                    WHERE city_list_member_table.city_list_id = location_criteria_table.city_list_id
                    AND location_location_type_table.location_type_id = location_criteria_table.location_type_id
                    AND location_list_table.location_list_id = criteria_table.location_list_id
                )
                AND city_list_member_table.city_list_id = location_criteria_table.city_list_id
                AND location_location_type_table.location_type_id = location_criteria_table.location_type_id
            )
            OR (
                location_criteria_table.location_id_old IS NOT NULL
                AND location_criteria_table.location_type_id IS NOT NULL
                AND EXISTS (
                    SELECT 1
                    FROM location.location_criteria_table
                    WHERE location_criteria_table.location_id_old = location_table.location_id
                    AND location_location_type_table.location_type_id = location_criteria_table.location_type_id
                )
                AND location_criteria_table.location_id_old = location_table.location_id
                AND location_location_type_table.location_type_id = location_criteria_table.location_type_id
            )
            OR (
                criteria_table.group_id IS NOT NULL
                AND EXISTS (
                    SELECT 1
                    FROM criteria.criteria_table
                    WHERE group_profile_table.group_id = criteria_table.group_id
                )
            )
            OR (
                criteria_table.group_list_id IS NOT NULL
                AND EXISTS (
                    SELECT 1
                    FROM criteria.criteria_table
                    WHERE group_list_member_table.group_list_id = criteria_table.group_list_id
                )
                AND group_list_member_table.group_list_id = criteria_table.group_list_id
            )
        GROUP BY
            criteria_profile_table.profile_id,
            criteria_profile_table.criteria_id
        HAVING
            criteria_profile_table.criteria_id != 9001
        ORDER BY
            criteria_profile_table.criteria_id;
    """

        gencrud.cursor.execute(query)
        table = gencrud.cursor.fetchall()
        table = pd.DataFrame(table)[0].to_list()
        string = "criteria_profile_id != "
        for i, o in enumerate(table):
            if i != len(table) - 1:
                string += str(o) + " AND criteria_profile_id != "
            else:
                string += str(o)

        crud = GenericCRUD(default_schema_name="criteria_profile")
        lis = crud.select_multi_value_by_where(
            view_table_name="criteria_profile_table",
            select_clause_value="criteria_profile_id",
            where=string,
            limit=limit_num,
        )
        return lis

