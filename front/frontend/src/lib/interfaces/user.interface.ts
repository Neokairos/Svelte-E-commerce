export interface Token {
	refresh?: string;
	access?: string;
}
export interface User {
	id?: string | null;
	email?: string;
	username?: string;
	password?: string;
	tokens?: Token;
	birth_date?: string;
	is_staff?: boolean;
	
}

export interface UserResponse {
	user?: User;
	status?: number;
}