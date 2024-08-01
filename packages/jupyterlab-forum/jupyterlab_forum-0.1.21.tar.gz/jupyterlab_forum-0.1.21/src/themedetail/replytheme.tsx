import { ShowThemeDetail } from '../showthemedetail';
import { PageConfig } from '@jupyterlab/coreutils';

export async function handleReplyToTheme(widget: any, username: string, themeId: string, forumEndpointUrl: string, replytext: any) {

  // Temporary HTML for the reply form
  const token = PageConfig.getToken();


  const newReply = {
    Content: replytext,
    Author: username,
    ThemeID: themeId,
    // Add other relevant fields if necessary
  };

  try {
    // Send reply data to the server
    const response = await fetch(forumEndpointUrl + "replytheme", {
      method: 'POST',
      body: JSON.stringify(newReply),
      headers: { 'Content-Type': 'application/json',
                 'Authorization': `token ${token}`,
               },
    });

    if (response.ok) {
      // Reply sent successfully
      const data = await response.json();
      const replyId = data.ReplyID;

      ShowThemeDetail(widget, themeId, forumEndpointUrl, username); // Show the details of the new theme
      // Optionally, display a confirmation message or update the UI
      console.log('Reply sent successfully with ID:', replyId);
      // You can call another function to update the UI with the new reply
    } else {
      // Handle errors here
      console.error('Failed to send reply:', response.status);
      ShowThemeDetail(widget, themeId, forumEndpointUrl, username); // Show the details of the new theme
    }
  } catch (error) {
    console.error('Error sending reply:', error);
    // Handle errors here
  }
}
