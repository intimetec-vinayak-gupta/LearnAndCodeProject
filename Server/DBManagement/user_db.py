from database_manager import DatabaseManager as db

class UserDB:
    def get_user_role(username, password):
        query = """
            SELECT u.Id, u.Name AS UserName, r.Name AS RoleName 
            FROM Users u 
            JOIN Roles r ON u.RoleId = r.Id  
            JOIN UsersCredentials uc ON u.Id = uc.UserId 
            WHERE u.Name = %s AND uc.Password = %s
        """
        return db.execute_query(query, (username, password))
    
    def fetchUserProfile(user_id):
        query = "SELECT diet_type, spice_level, preference, sweet_tooth FROM Userprofile WHERE user_id = %s;"
        return db.execute_query(query, (user_id,))
