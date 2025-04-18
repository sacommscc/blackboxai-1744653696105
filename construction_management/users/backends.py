from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
import logging

logger = logging.getLogger(__name__)

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        try:
            # Handle both username and email parameters
            email = kwargs.get('email') or username
            logger.info(f"Attempting authentication with email: {email}")
            
            if not email or not password:
                logger.warning("Email or password is missing")
                return None

            try:
                user = UserModel.objects.get(email=email)
                logger.info(f"Found user with email: {email}")
                
                if user.check_password(password):
                    logger.info(f"Password check successful for user: {email}")
                    return user
                else:
                    logger.warning(f"Invalid password for user: {email}")
                    return None
                    
            except UserModel.DoesNotExist:
                logger.warning(f"No user found with email: {email}")
                return None
                
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(pk=user_id)
            logger.info(f"Retrieved user with id: {user_id}")
            return user if self.user_can_authenticate(user) else None
        except UserModel.DoesNotExist:
            logger.warning(f"No user found with id: {user_id}")
            return None
