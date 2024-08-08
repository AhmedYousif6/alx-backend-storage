-- creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student.

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score = 0;
    DECLARE total_projects = 0;

    SELECT SUM(score)
    INTO total_score
    FROM corrections
    WHERE corrections.user_id = user_id;

    SELECT COUNT(*)
    INTO total_projects
    FROM corrections
    WHERE corrections.user_id = user_id;

    UPDATE users
    SET users.average_score = IF(total_projects = 0, 0, total_score / total_projects);
    WHERE users.id = user_id;
END$$
DELIMITTER ;
