import { PageConfig } from '@jupyterlab/coreutils';
import {displayCurrentPageThemes} from './displayCurrentPageThemes'
import {updatePaginationControls} from './updatePaginationControls'

export async function fetchAndDisplayThemes(widget: any, forumEndpointUrl: string) {

    const token = PageConfig.getToken();

    try {
        const response = await fetch(forumEndpointUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `token ${token}`,
            },
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        widget.allThemes = data.themes;
        widget.showThemes = data.themes;

    } catch (error) {
        console.error('Error fetching themes:', error);
        const exampleThemes = [
          {
             ThemeID: 1,
             Title: "Example Theme 1",
             Author: "Admin",
             CreationTime: "2024-07-01T10:00:00",
             Status: "Open",
             Sticky: 1,
             Commentable : 0
           },
           {
             ThemeID: 2,
             Title: "Example Theme 2",
             Author: "User123",
             CreationTime: "2024-07-15T15:30:00",
             Status: "Closed",
             Sticky: 0,
             Commentable : 1
           },
           {
             ThemeID: 3,
             Title: "Example Theme 3",
             Author: "User123",
             CreationTime: "2024-07-15T15:30:00",
             Status: "Closed",
             Sticky: 0,
             Commentable : 1
           },
           {
             ThemeID: 4,
             Title: "Example Theme 4",
             Author: "User123",
             CreationTime: "2024-07-15T15:30:00",
             Status: "Closed",
             Sticky: 0,
             Commentable : 1
           },
           {
             ThemeID: 5,
             Title: "Example Theme 5",
             Author: "User123",
             CreationTime: "2024-07-15T15:30:00",
             Status: "Closed",
             Sticky: 0,
             Commentable : 1
           },
           {
             ThemeID: 6,
             Title: "Example Theme 6",
             Author: "User123",
             CreationTime: "2024-07-15T15:30:00",
             Status: "Closed",
             Sticky: 0,
             Commentable : 1
           },
           {
             ThemeID: 7,
             Title: "Example Theme 7",
             Author: "User123",
             CreationTime: "2024-07-15T15:30:00",
             Status: "Closed",
             Sticky: 0,
             Commentable : 1
           },

        ];

        widget.showThemes = exampleThemes;
        widget.allThemes = exampleThemes;
    }


    displayCurrentPageThemes(widget, 1, widget.themesPerPage, widget.showThemes);
    updatePaginationControls(widget, widget.allThemes.length, widget.themesPerPage);
}
