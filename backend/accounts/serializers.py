
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    """
    User registration serializer.
    
    Handles the process of creating new user accounts and includes custom validation logic
    such as password validation and tag selection validation.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)  # Password confirmation field

    class Meta:
        model = CustomUser  # Using CustomUser model
        fields = ('username', 'email', 'nickname', 'password', 'password2', 'gender', 'age_group', 'selected_tags')  # Include all fields

    def validate(self, attrs):
        """
        Validate the data.
        
        Verifies password matching and the number of selected tags.
        
        Parameters:
            attrs: Dictionary of data to validate
            
        Returns:
            Dictionary of validated data
            
        Raises:
            ValidationError: If passwords don't match or tag selection is invalid
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})  # Password matching validation
        
        # Tag selection validation (3-7 tags)
        selected_tags = attrs.get('selected_tags', [])
        if selected_tags and (len(selected_tags) < 3 or len(selected_tags) > 7):
            raise serializers.ValidationError({"selected_tags": "You must select between 3 and 7 tags."})  # Tag count validation
            
        return attrs

    def create(self, validated_data):
        """
        Create a user with validated data.
        
        Parameters:
            validated_data: Validated user data
            
        Returns:
            Newly created CustomUser instance
        """
        validated_data.pop('password2')  # Don't store password2
        user = CustomUser.objects.create_user(**validated_data)  # Create user
        return user
