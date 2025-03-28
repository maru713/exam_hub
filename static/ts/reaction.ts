document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll<HTMLButtonElement>('.reaction-button').forEach(button => {
    button.addEventListener('click', async (event) => {
      event.preventDefault();

      const answerId = button.dataset.answerId;
      const reactionType = button.dataset.reactionType;

      if (!answerId || !reactionType) return;

      try {
        const response = await fetch(`/problems/answers/${answerId}/react/${reactionType}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCSRFToken(),
            'X-Requested-With': 'XMLHttpRequest',
          },
        });

        if (response.ok) {
          location.reload(); // 簡易的にページを更新（後でDOMだけ更新にしてもOK）
        } else {
          console.error('リアクション失敗');
        }
      } catch (err) {
        console.error('通信エラー:', err);
      }
    });
  });
});

function getCSRFToken(): string {
  const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
  return cookie ? cookie.split('=')[1] : '';
}