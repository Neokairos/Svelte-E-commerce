import axios from 'axios';
import { browser } from '$app/environment';
import { goto } from '$app/navigation';
import type { Token, UserResponse } from '$lib/interfaces/user.interface';
import type { CustomError } from '$lib/interfaces/error.interface';
import { notificationData, notificationErrorData } from '$lib/store/notificationStore';
import { userData } from '$lib/store/userStore';
import { variables } from '$lib/utils/constants';
import { formatText } from '$lib/formats/formatString';

export const browserGet = (key: string): string | undefined => {
    if (localStorage) {
        const item = localStorage.getItem(key);
        if (item) {
            return item;
        }
    } else {
    console.log('localStorage returned false');
    return undefined

}};


export const browserSet = (key: string, value: string): void => {
    if (browser) {
        localStorage.setItem(key, value);
    }
};


export const post = async (
    url: string,
    body: unknown,
): Promise<[object, Array<CustomError>, number]> => { // Updated return type
    try {
        const headers = { 'Authorization': '' };
        const token = browserGet('refreshToken');
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        const res = await axios.post(url, body, { headers });
        const response = res.data;
        const status = res.status; // Capture the status

        if (status === 200 || status === 201) {
            return [response, [], status];

        } else {
            const error = response.data.user
            const emailError = error.email ? error.email[0] : null; 
            const nameError  = error.username ? error.username[0] : null;

            if (nameError) {
                return [{}, nameError, status]
            } 
            else if (emailError) {
                return [{}, emailError, status]
            } 
            else if (nameError || emailError) {
                return [{}, [nameError,emailError], status ]}

            return [{}, error, status]
        }
    } catch (error: any) {
        if (error.response && error.response.data) {
            const errors: Array<CustomError> = [];
            if (error.response.data.user.username) {
                const username_error = error.response.data.user.username

                errors.push({ error: username_error });
            }
            if (error.response.data.user.email) {
                const email_error = error.response.data.user.email

                errors.push({ error: email_error });
            }
            // Return an empty object, the errors array, and the status
            return [{}, errors, error.response.status];
        }

        // If the error does not have the expected structure, return a default error
        return [{}, [{ error: "An unexpected error occurred." }], 500]; // Assuming a generic error status
    }
};



export const getCurrentUser = async (
    refreshUrl: string,
    userUrl: string
): Promise<[object, Array<CustomError>]> => {

    //getting the refresh token and passing the localStorage token as second argument
    if (browserGet('refreshToken')){

        const jsonRes = await axios.post(refreshUrl, {
            refresh: `${browserGet('refreshToken')}`
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const accessRefresh: Token = jsonRes.data.access;
        console.log(accessRefresh)
        //get request on UserRetrieveAPIView with the access token
        if (accessRefresh) {
            
            const res = await axios.post(userUrl,{/*payload body data arg*/ }, {
                headers: {
                    Authorization: `Bearer ${accessRefresh}`
                }
            });
            //breaks here
            if (res.status >= 400) {
                const data = res.data;
                const error = data.user.error[0];
                return [{}, error];
            }
            console.log('nigga: ',res.data)

            const response = res.data;
            return [response.user, []];
    }   else {
            return [{}, [{ error: 'Refresh token is invalid...' }]];
    }
}
    else {
        return [{}, [{error:'No refresh token found'}]]
}};

export const logOutUser = async (): Promise<void> => {
    //authenticating first
    const res = await axios.post(`${variables.BASE_API_URI}/token/refresh`, {
        refresh: `${browserGet('refreshToken')}`
    }, {
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const accessRefresh = res.data;
    const jres = await axios.post(`${variables.BASE_API_URI}/logout`, {
        refresh: `${browserGet('refreshToken')}`
    }, {
        headers: {
            Authorization: `Bearer ${accessRefresh.access}`,
            'Content-Type': 'application/json'
        }
    });
    if (jres.status !== 204) {
        const data = jres.data;
        const error = data.user.error[0];
        throw { id: error.id, message: error };
    }
    localStorage.removeItem('refreshToken');
    userData.set({});
    notificationData.update(() => 'You have successfully logged out...');
    await goto('/accounts/login');
};
export const handlePostRequestsWithPermissions = async (
    targetUrl: string,
    body: unknown,
    method = 'POST'
): Promise<[object, Array<CustomError>]> => {
    const res = await axios.post(`${variables.BASE_API_URI}/token/refresh`, {
        refresh: `${browserGet('refreshToken')}`
    }, {
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const accessRefresh = res.data;
    const jres = await axios({
        method: method,
        url: targetUrl,
        data: body,
        headers: {
            Authorization: `Bearer ${accessRefresh.access}`,
            'Content-Type': 'application/json'
        }
    });

    switch (method) {
        case 'PATCH':
            if (jres.status !== 200) {
                const data = jres.data;
                const errs = data.errors;
                return [{}, errs];
            }
            return [jres.data, []];
        case 'POST':
            if (jres.status !== 201) {
                const data = jres.data;
                const errs = data.errors;
                return [{}, errs];
            }
            return [jres.data, []];
        default:
            throw new Error(`Unsupported method: ${method}`);
    }
};

export const UpdateField = async (
    fieldName: string,
    fieldValue: string,
    url: string
): Promise<[object, Array<CustomError>]> => {
    const userObject: UserResponse = { user: {} };
    let formData: UserResponse | any;
    if (url.includes('/user/')) {
        formData = userObject;
        formData['user'][`${fieldName}`] = fieldValue;
    } else {
        formData[`${fieldName}`] = fieldValue;
    }

    const [response, err] = await handlePostRequestsWithPermissions(url, formData, 'PATCH');
    if (err.length > 0) {
        return [{}, err];
    }
    notificationData.update(() => `${formatText(fieldName)} has been updated successfully.`);
    return [response, []];
};
