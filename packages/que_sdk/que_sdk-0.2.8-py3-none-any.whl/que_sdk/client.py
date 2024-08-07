import http
from typing import (
    Any,
    BinaryIO,
    Literal,
)

from que_sdk.clients import (
    AuthClient,
    PhotoClient,
    ProfileClient,
    RoleClient,
    UserClient,
)
# noinspection PyProtectedMember
from que_sdk.schemas import (
    LoginSchema,
    ProfileCreateSchema,
    ProfileUpdateSchema,
    ResetPasswordSchema,
    RoleSchema,
    SignUpSchema,
    TMELoginSchema,
    UserSchema,
)
from que_sdk.types import (
    FlexibleResponseT,
    ResponseT,
)

__all__ = ("QueClient",)


class QueClient:
    def __init__(self) -> None:
        self._clients = {
            "auth": AuthClient(),
            "user": UserClient(),
            "role": RoleClient(),
            "profile": ProfileClient(),
            "photo": PhotoClient(),
        }

    def get_client(
            self, *, client_name: Literal["auth", "user", "role", "profile", "photo"]
    ) -> Any:
        if client_name not in self._clients:
            raise ValueError(f"Unknown client: {client_name}")
        return self._clients[client_name]

    async def signup(self, *, data_in: SignUpSchema) -> ResponseT[dict[str, Any]]:
        """
        Register a new user.

        :param data_in: SignUpSchema object containing user registration data, including
                        username, telegram_id (optional), and password (optional)
        :return: status code and response dictionary with user data
        """
        client = self.get_client(client_name="auth")
        return await client.signup(data_in=data_in)

    async def login_t_me(self, *, data_in: TMELoginSchema) -> ResponseT[dict[str, Any]]:
        """
         Login to the user's telegram account.

        :param data_in: TMELoginSchema object containing TME login data, including
                        telegram_id, signature, nonce, and timestamp
        :return: status code and response dictionary with access and refresh token
        """
        client = self.get_client(client_name="auth")
        return await client.login_t_me(data_in)

    async def login(self, *, data_in: LoginSchema) -> ResponseT[dict[str, Any]]:
        """
        Login to the user's account.

        :param data_in: LoginSchema object containing login data, including
                        username and password
        :return: status code and response dictionary with access token and user data
        """
        client = self.get_client(client_name="auth")
        return await client.login(data_in)

    async def reset_password(
            self,
            *,
            data_in: ResetPasswordSchema,
    ) -> ResponseT[str]:
        """
        Reset user password.

        :param data_in: ResetPasswordSchema object containing old password, new password,
                        and repeated new password
        :return: status code and response message
        """
        client = self.get_client(client_name="auth")
        return await client.reset_password(data_in)

    async def get_users(self) -> ResponseT[list[dict[str, Any]]]:
        """
        Get a list of all users.

        :return: status code and list of users
        """
        client = self.get_client(client_name="user")
        return await client.get_users()

    async def get_user_me(
            self,
            *,
            access_token: str,
    ) -> ResponseT[dict[str, Any]]:
        """
        Get information about the current user.

        :param access_token: access token
        :return: status code and user information
        """
        client = self.get_client(client_name="user")
        return await client.get_user_me(access_token)

    async def update_user_me(
            self,
            *,
            data_in: UserSchema,
    ) -> ResponseT[dict[str, Any]]:
        """
        Update information about the current user.

        :param data_in: user data to update
        :return: status code and updated user information
        """
        client = self.get_client(client_name="user")
        return await client.update_user_me(data_in)

    async def deactivate_user_me(
            self,
            *,
            access_token: str,
    ) -> http.HTTPStatus:
        """
        Deactivate the current user.

        :param access_token: access token
        :return: status code
        """
        client = self.get_client(client_name="user")
        return await client.deactivate_user_me(access_token)

    async def reactivate_user(
            self,
            *,
            access_token: str,
    ) -> http.HTTPStatus:
        """
        Reactivate the current user.

        :param access_token: access token
        :return: status code
        """
        client = self.get_client(client_name="user")
        return await client.reactivate_user(access_token)

    async def create_role(
            self,
            *,
            data_in: RoleSchema,
            access_token: str,
    ) -> ResponseT[dict[str, Any]]:
        """
        Create a new role.

        :param data_in: RoleSchema object containing role data, including title
        :param access_token: access token for authentication
        :return: status code and response dictionary with role data
        """
        client = self.get_client(client_name="role")
        return await client.create_role(data_in, access_token)

    async def get_role_or_roles(
            self,
            *,
            role_id: int | None = None,
            title: str | None = None,
    ) -> ResponseT[FlexibleResponseT]:
        """
        Get roles based on role_id or title.

        :param role_id: role ID to filter roles by (optional)
        :param title: role title to filter roles by (optional)
        :return: status code and response, either a list of roles or a single role
        """
        client = self.get_client(client_name="role")
        return await client.get_roles(role_id, title)

    async def update_role_by_id(
            self,
            *,
            role_id: int,
            new_title: str,
            access_token: str | None = None,
    ) -> ResponseT[dict[str, Any]]:
        """
        Update a role's title by its ID.

        :param role_id: role ID to update
        :param new_title: new title for the role
        :param access_token: access token for authentication (optional)
        :return: status code and response dictionary with updated role data
        """
        client = self.get_client(client_name="role")
        return await client.update_role_by_id(
            role_id=role_id, new_title=new_title, access_token=access_token
        )

    async def delete_role_by_id(
            self,
            *,
            role_id: int,
            access_token: str | None = None,
    ) -> http.HTTPStatus:
        """
        Delete a role by its ID.

        :param role_id: role ID to delete
        :param access_token: access token for authentication (optional)
        :return: status code
        """
        client = self.get_client(client_name="role")
        return await client.delete_role_by_id(
            role_id=role_id, access_token=access_token
        )

    async def create_profile(
            self,
            *,
            data_in: ProfileCreateSchema,
            access_token: str,
    ) -> ResponseT[dict[str, Any]]:
        client = self.get_client(client_name="profile")
        return await client.create_profile(data_in=data_in, access_token=access_token)

    async def get_profile(
            self, *, user_id: int, access_token: str
    ) -> ResponseT[dict[str, Any]]:
        client = self.get_client(client_name="profile")
        return await client.get_profile(user_id=user_id, access_token=access_token)

    async def update_profile(
            self,
            *,
            profile_id: int,
            data_in: ProfileUpdateSchema,
            access_token: str,
    ) -> ResponseT[dict[str, Any]]:
        client = self.get_client(client_name="profile")
        return await client.update_profile(
            profile_id=profile_id, data_in=data_in, access_token=access_token
        )

    async def delete_profile(
            self,
            *,
            profile_id: int,
            access_token: str,
    ) -> http.HTTPStatus:
        client = self.get_client(client_name="profile")
        return await client.delete_profile(profile_id, access_token=access_token)

    async def upload_photo(
            self,
            *,
            file: BinaryIO | bytes,
            access_token: str,
            filename: str | None = None,
    ) -> ResponseT[dict[str, Any]]:
        client = self.get_client(client_name="photo")
        return await client.upload_photo(
            access_token=access_token, file=file, filename=filename
        )

    async def get_all_photos(
            self,
            *,
            access_token: str,
    ) -> ResponseT[list[dict[str, Any]]]:
        client = self.get_client(client_name="photo")
        return await client.get_all_photos(access_token=access_token)

    async def get_photo_by_id(self, *, photo_id: int, access_token: str) -> ResponseT[dict[str]]:
        client = self.get_client(client_name="photo")
        return await client.get_photo_by_id(photo_id=photo_id, access_token=access_token)
