import Quill from 'quill';
import 'quill/dist/quill.snow.css';

export function initializeQuill(widget: any): Quill {
    const quill = new Quill('#themeDescription', {
      theme: 'snow',
      modules: {
        toolbar: [
          [{ 'header': [1, 2, false] }],
          ['bold', 'italic', 'underline'],
          ['link', 'image'],
          [{ 'list': 'ordered'}, { 'list': 'bullet' }]
        ]
      }
    });

    return quill
}
