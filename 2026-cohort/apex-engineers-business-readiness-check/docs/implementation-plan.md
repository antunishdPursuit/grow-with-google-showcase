# Business Readiness Check Implementation Plan

## Objective

Deliver a publicly deployable Python application that lets a small-business
owner complete a four-question technology assessment, receive a weighted risk
result, identify the highest-priority gap, and download recommended next steps.

## Scope

The minimum version includes:

- Four fixed diagnostic questions.
- Yes, No, and Not applicable answers.
- Weighted scoring and project-designed risk categories.
- Prioritized recommendations.
- A plain-text report download.
- Automated scoring tests.
- Privacy, security, and evidence limitations.

Accounts, databases, file uploads, third-party APIs, vendor comparisons, and
actual system integrations are outside this version.

## Implementation Steps

1. Implement the question definitions, validation, scoring, prioritization, and
   report functions in `diagnostic.py`.
2. Verify the rules and edge cases in `tests/test_diagnostic.py`.
3. Connect the verified functions to a single-page Streamlit form in `app.py`.
4. Add privacy text, input limits, safe all-not-applicable behavior, and a
   general-guidance disclaimer.
5. Complete the README, security note, project summary, and MIT license.
6. Test the complete local user journey and report download.
7. Deploy publicly and repeat the complete user journey on the live URL.
8. Record the walkthrough and add its link to the README.
9. Review the final repository, push the branch, and open the required pull
   request without merging it.

## Timeline

| Date | Work |
| --- | --- |
| August 10 | Build the scoring core, tests, application, and documentation. |
| August 11 | Complete local user-flow testing and correct defects. |
| August 12 | Deploy publicly and verify the live application. |
| August 13 | Freeze features, finish the summary, and record the walkthrough. |
| August 14 | Verify links and files, push final changes, and open the pull request before 11:59 PM Eastern. |

## Resources

- Python 3.10 or newer.
- Streamlit for the web interface and public application.
- Python `unittest` and Pytest for automated verification.
- Git and GitHub for version control and submission.
- The team project report for the diagnostic questions and weights.
- The MMC BUILD Project Outline for submission requirements.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Arbitrary thresholds appear scientifically validated | Label them as project-designed categories in the app and documentation. |
| Not applicable answers distort the score | Exclude their weights from the denominator and test the calculation. |
| Every answer is not applicable | Return no score and ask for at least one applicable area. |
| User enters sensitive information | Make business details optional, prohibit sensitive data, and avoid persistent storage. |
| User input affects the report | Normalize and length-limit optional text; use plain-text output. |
| Solo implementation misses defects | Keep the application small and use automated and manual checks. |
| Public deployment behaves differently | Repeat the golden path and failure checks on the live URL. |
| Deadline pressure causes scope growth | Keep integrations, uploads, vendor comparison, and PDF output outside the MVP. |

## Verification

The solution is ready for submission only when:

- Automated tests pass.
- The local and deployed applications complete the full assessment flow.
- Missing answers and all-not-applicable answers fail safely.
- The downloaded report matches the displayed result.
- Documentation claims match observed behavior.
- No secret, private data, cache, or local environment file is tracked.
- The walkthrough is no longer than five minutes.
- The final pull request is open against upstream `main` and remains unmerged.

