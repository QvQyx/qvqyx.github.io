using System.Collections;
using UnityEngine;
using UnityEngine.SceneManagement;

// Cleaned portfolio excerpt based on the original Unity scripts for 0428.
// Each clickable model part cycles through forms. The puzzle clears when the
// combined model shape matches the target shadow silhouette.

public class ClickParityModelPart : MonoBehaviour
{
    [SerializeField] private GameObject[] formStates;
    [SerializeField] private int startingClickCount = 2;
    [SerializeField] private int matchingParity = 1;

    public bool MatchesShadow { get; private set; }

    private int clickCount;

    private void Start()
    {
        clickCount = startingClickCount;
        ApplyCurrentForm();
    }

    private void OnMouseDown()
    {
        if (!Input.GetMouseButtonDown(0)) return;

        clickCount += 1;
        ApplyCurrentForm();
    }

    private void ApplyCurrentForm()
    {
        if (formStates.Length > 0)
        {
            int activeIndex = clickCount % formStates.Length;

            for (int i = 0; i < formStates.Length; i++)
            {
                formStates[i].SetActive(i == activeIndex);
            }
        }

        MatchesShadow = clickCount % 2 == matchingParity;
        Debug.Log($"{name} matches shadow: {MatchesShadow}");
    }
}

public class ShadowMatchCompletion : MonoBehaviour
{
    [SerializeField] private ClickParityModelPart[] requiredParts;
    [SerializeField] private GameObject completeMessage;
    [SerializeField] private int nextSceneIndex = 3;

    private bool hasCompleted;

    private void Update()
    {
        if (hasCompleted || !AllPartsMatchShadow()) return;

        hasCompleted = true;
        completeMessage.SetActive(true);
        StartCoroutine(LoadNextSceneAfterDelay());
    }

    private bool AllPartsMatchShadow()
    {
        foreach (ClickParityModelPart part in requiredParts)
        {
            if (!part.MatchesShadow) return false;
        }

        return true;
    }

    private IEnumerator LoadNextSceneAfterDelay()
    {
        yield return new WaitForSeconds(3f);
        SceneManager.LoadScene(nextSceneIndex);
    }
}
