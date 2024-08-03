import {ShowThemeDetail} from '../showthemedetail'

export async function toggletheme(widget: any, username: string, themeId: string, themeStatus: string ,forumEndpointUrl: string, token: any) {
  try {
      const newStatus = themeStatus === 'Open' ? 'Closed' : 'Open';
      const response = await fetch(`${forumEndpointUrl}/togglestatus`, {
          method: 'PATCH',
          headers: {
              'Content-Type': 'application/json',
              'Authorization': `token ${token}`,
          },
          body: JSON.stringify({ ThemeID: themeId, Status: newStatus }),
      });

      if (response.ok) {
          ShowThemeDetail(widget, themeId, forumEndpointUrl, username); // Refresh the theme detail
      } else {
          console.error('Failed to toggle status:', response.status);
      }
  } catch (error) {
      console.error('Error toggling status:', error);
  }
}
