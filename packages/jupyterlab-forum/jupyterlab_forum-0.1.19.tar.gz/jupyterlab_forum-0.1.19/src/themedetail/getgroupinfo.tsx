import { PageConfig } from '@jupyterlab/coreutils';
export async function fetchGroupData(forumEndpointUrl: string): Promise<string[]> {

    const newPath = '/jupyterhub/hub/api/groups/dozent';
    const url = new URL(forumEndpointUrl);
    url.pathname = newPath;

    const token = PageConfig.getToken();

    if (!token) {
    throw new Error('API token is not available from PageConfig.');
    }

    let responseData: any;

    try {
        const response = await fetch(url.toString(), {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `token ${token}`,
            }
        });

        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }

        responseData = await response.json();
        console.log('Response Data:', responseData);



    } catch (error) {
        console.error('Error fetching data:', error);
        responseData = {"users": [error]}
    }

    // You can use responseData variable here or return it from the function if needed
    return responseData["users"]
}
