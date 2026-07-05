interface PlaceholderTabProps {
  title: string
  description: string
}

export function PlaceholderTab({ title, description }: PlaceholderTabProps) {
  return (
    <div className="tab-panel placeholder-tab">
      <h3 className="resume-heading">{title}</h3>
      <p>{description}</p>
      <p className="placeholder-status">&gt;&gt; MODULE UNDER CONSTRUCTION</p>
    </div>
  )
}
