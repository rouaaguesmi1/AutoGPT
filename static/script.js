// static/script.js (Version 2 avec Onglets)
document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('.agent-form');
    const resultsArea = document.getElementById('results-area');
    const renderedOutput = document.getElementById('renderedOutput');

    forms.forEach(form => {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const agent = form.dataset.agent;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            const button = form.querySelector('button[type="submit"]');
            const originalButtonText = button.textContent;
            button.disabled = true;
            button.textContent = 'En cours...';

            resultsArea.classList.add('d-none'); // Cache les anciens résultats

            try {
                // Note : nous aurons besoin de créer cet endpoint `/execute_agent`
                const response = await fetch('/execute_agent', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ agent, ...data })
                });

                const result = await response.json();

                if (response.ok) {
                    // Utilise marked.js pour afficher le Markdown en HTML
                    renderedOutput.innerHTML = marked.parse(result.output || 'Aucun résultat textuel.');
                    resultsArea.classList.remove('d-none');
                } else {
                    renderedOutput.innerHTML = `<p class="text-danger">Erreur: ${result.detail || 'Erreur inconnue'}</p>`;
                    resultsArea.classList.remove('d-none');
                }

            } catch (error) {
                renderedOutput.innerHTML = `<p class="text-danger">Erreur de connexion: ${error.message}</p>`;
                resultsArea.classList.remove('d-none');
            } finally {
                button.disabled = false;
                button.textContent = originalButtonText;
            }
        });
    });
});