import {fetchAndDisplayThemes} from '../forumdashboard/fetchAndDisplayThemes'

export async function deletetheme(widget: any, themeId: string, forumEndpointUrl: string, token: any) {
  const userConfirmed = window.confirm("Are you sure you want to delete this theme?");
  if (!userConfirmed) {
    return; // User cancelled the deletion
  }

    try {
        const response = await fetch(`${forumEndpointUrl}/deletetheme`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `token ${token}`,
            },
            body: JSON.stringify({ ThemeID: themeId }),
        });

        if (response.ok) {
            widget.node.innerHTML = widget.originalHTML;
            fetchAndDisplayThemes(widget, forumEndpointUrl);
        } else {
            console.error('Failed to delete theme:', response.status);
        }
    } catch (error) {
        console.error('Error deleting theme:', error);
    }
}
