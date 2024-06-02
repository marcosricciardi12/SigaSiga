import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class VideoStreamService {

  constructor() { }

  async startVideoStream(url: string, token: string, onFrame: (blob: Blob) => void) {
    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    const reader = response.body?.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';

    while (true) {
      const { value, done } = await reader?.read()!;

      if (done) {
        console.log('Stream finished');
        break;
      }

      buffer += decoder.decode(value, { stream: true });

      let boundaryIndex;
      while ((boundaryIndex = buffer.indexOf('--frame')) !== -1) {
        const frameEndIndex = buffer.indexOf('--frame', boundaryIndex + 1);
        if (frameEndIndex === -1) break;

        const frameData = buffer.substring(boundaryIndex, frameEndIndex);
        const blob = new Blob([frameData], { type: 'image/jpeg' });
        onFrame(blob);

        buffer = buffer.substring(frameEndIndex);
      }
    }
  }
}