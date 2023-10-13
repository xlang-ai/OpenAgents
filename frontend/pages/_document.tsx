import { DocumentProps, Head, Html, Main, NextScript } from 'next/document';

type Props = DocumentProps & {
  // add custom document props
};

export default function Document(props: Props) {
  return (
    <Html lang='en'>
      <Head>
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-title" content="OpenAgents"></meta>
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
