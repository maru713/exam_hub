document.addEventListener('DOMContentLoaded', () => {
  document.addEventListener('click', (event) => {
    const button = (event.target as HTMLElement).closest<HTMLButtonElement>('.reaction-button');
    if (!button) return;

    console.log('リアクションボタン押した');
    event.preventDefault();

    const answerId = button.dataset.answerId;
    const reactionType = button.dataset.reactionType;

    if (!answerId || !reactionType) return;

    const icon = button.querySelector('i');
    const countSpan = button.querySelector('span');

    if (icon) {
      if (icon.classList.contains('far')) {
        icon.classList.remove('far');
        icon.classList.add('fas');
      } else if (icon.classList.contains('fas')) {
        icon.classList.remove('fas');
        icon.classList.add('far');
      }
    }

    if (countSpan && icon) {
      const currentCount = parseInt(countSpan.textContent || '0', 10);
      const newCount = icon.classList.contains('fas') ? currentCount + 1 : currentCount - 1;
      countSpan.textContent = newCount.toString();
    }

    fetch(`/problems/answers/${answerId}/react/${reactionType}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCSRFToken(),
        'X-Requested-With': 'XMLHttpRequest',
      },
    }).catch(err => {
      console.error('通信エラー:', err);
    });
  });
});

function getCSRFToken(): string {
  const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
  return cookie ? cookie.split('=')[1] : '';
}