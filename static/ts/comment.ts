document.addEventListener('DOMContentLoaded', () => {
  console.log('DOMContentLoaded: JS is loaded and ready.');  // ★1

  document.querySelectorAll('.comment-form').forEach((form) => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      console.log('Submit event triggered.');  // ★2

      const targetForm = e.target as HTMLFormElement;
      const formData = new FormData(targetForm);

      // フォームデータの中身を表示 (Key/Valueの一覧)
      console.log('FormData entries:', Array.from(formData.entries()));  // ★3

      const action = targetForm.action;
      console.log('Action endpoint:', action);  // ★4

      try {
        console.log('Sending fetch request...');  // ★5
        const response = await fetch(action, {
          method: 'POST',
          body: formData,
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        });

        console.log('Fetch response received, status:', response.status);  // ★6

        if (response.ok) {
          // Django側が返す JSON をパース
          const result = await response.json();
          console.log('Server JSON response:', result);  // ★7

          const commentSection = targetForm.closest('.card')?.querySelector('.comment-list');
          if (commentSection) {
            // 画面にDOM要素を追加
            console.log('Appending new comment to .comment-list');  // ★8
            const newComment = document.createElement('div');
            newComment.className = "border-bottom pb-1 mb-1";
            newComment.innerHTML = `
              <strong>${result.username}</strong>: ${result.body}
              <span class="text-muted comment-timestamp">（${result.created_at}）</span>
            `;
            commentSection.appendChild(newComment);

            commentSection.scrollTop = commentSection.scrollHeight;
          } else {
            console.warn('Could not find .comment-list.');  // ★9
          }

          // テキストエリアをクリア
          (targetForm.querySelector('textarea') as HTMLTextAreaElement).value = '';
        } else {
          console.error('投稿失敗', response.status);  // ★10
        }
      } catch (error) {
        console.error('送信エラー:', error);  // ★11
      }
    });
  });
});