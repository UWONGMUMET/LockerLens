import JobSummaryCard from './JobSummaryCard.jsx';
import MissingInfoSummaryCard from './MissingInfoSummaryCard.jsx';
import MissingInformationOnlyCard from './MissingInformationOnlyCard.jsx';
import PersonalDataWarningCard from './PersonalDataWarningCard.jsx';
import QuestionsToAskCard from './QuestionsToAskCard.jsx';
import RecommendedActionCard from './RecommendedActionCard.jsx';
import RedFlagAccordion from './RedFlagAccordion.jsx';
import SafeApplyChecklistCard from './SafeApplyChecklistCard.jsx';
import ScoreBreakdownCard from './ScoreBreakdownCard.jsx';
import SourceReferenceCard from './SourceReferenceCard.jsx';
import TrustScoreCard from './TrustScoreCard.jsx';

function SourceBlock({ result }) {
  if (!result.source_url && !result.keywords_checked?.length) return null;
  return <SourceReferenceCard result={result} />;
}

function PersonalWarningBlock({ result }) {
  if (!result.personal_data_warning?.is_detected) return null;
  return <PersonalDataWarningCard warning={result.personal_data_warning} />;
}

export default function ScanResultSections({ result, compact = false }) {
  if (!result) return null;

  if (compact) {
    return (
      <div className="space-y-4">
        <TrustScoreCard result={result} />
        <ScoreBreakdownCard items={result.score_breakdown || []} />
        <RecommendedActionCard action={result.recommended_action} note={result.safety_note} />
        <PersonalWarningBlock result={result} />
        <MissingInformationOnlyCard items={result.missing_information || []} />
        <MissingInfoSummaryCard
          summary={result.missing_information_summary}
          items={result.missing_information || []}
        />
        <RedFlagAccordion flags={result.red_flags || []} />
        <QuestionsToAskCard items={result.questions_to_ask_recruiter || []} />
        <SafeApplyChecklistCard items={result.safe_apply_checklist || []} />
        <SourceBlock result={result} />
      </div>
    );
  }

  return (
    <>
      <div className="grid grid-cols-1 gap-4 lg:hidden">
        <TrustScoreCard result={result} />
        <ScoreBreakdownCard items={result.score_breakdown || []} />
        <RecommendedActionCard action={result.recommended_action} note={result.safety_note} />
        <PersonalWarningBlock result={result} />
        <JobSummaryCard summary={result.job_summary} />
        <MissingInformationOnlyCard items={result.missing_information || []} />
        <MissingInfoSummaryCard
          summary={result.missing_information_summary}
          items={result.missing_information || []}
        />
        <RedFlagAccordion flags={result.red_flags || []} />
        <QuestionsToAskCard items={result.questions_to_ask_recruiter || []} />
        <SafeApplyChecklistCard items={result.safe_apply_checklist || []} />
        <SourceBlock result={result} />
      </div>

      <div className="hidden gap-6 lg:grid lg:grid-cols-12 lg:items-start">
        <div className="space-y-4 lg:col-span-7">
          <JobSummaryCard summary={result.job_summary} />
          <MissingInformationOnlyCard items={result.missing_information || []} />
          <MissingInfoSummaryCard
            summary={result.missing_information_summary}
            items={result.missing_information || []}
          />
          <RedFlagAccordion flags={result.red_flags || []} />
          <QuestionsToAskCard items={result.questions_to_ask_recruiter || []} />
        </div>

        <aside className="space-y-4 lg:col-span-5 lg:self-start">
          <TrustScoreCard result={result} />
          <ScoreBreakdownCard items={result.score_breakdown || []} />
          <RecommendedActionCard action={result.recommended_action} note={result.safety_note} />
          <PersonalWarningBlock result={result} />
          <SafeApplyChecklistCard items={result.safe_apply_checklist || []} />
          <SourceBlock result={result} />
        </aside>
      </div>
    </>
  );
}
