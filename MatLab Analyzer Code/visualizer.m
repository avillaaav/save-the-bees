clc,
clear,
N = 1;
for ii = 1: N
    waveFile=([ num2str(ii) '.wav']);
    for jj  = 1:size(N,1)
        au=myAudioRead(waveFile); y=au.signal; fs=au.fs;
        frameSize = 256;
        overlap = 128;
        y=y-mean(y);				% zero-mean substraction
        frameMat=buffer2(y, frameSize, overlap);	% frame blocking
        frameNum=size(frameMat, 2);			% no. of frames
        volume=frame2volume(frameMat);		% volume
        volumeTh1=max(volume)*0.1;			% volume threshold 1
        volumeTh2=median(volume)*0.1;			% volume threshold 2
        volumeTh3=min(volume)*10;			% volume threshold 3
        volumeTh4=volume(1)*5;				% volume threshold 4
        index1 = find(volume>volumeTh1);
        index2 = find(volume>volumeTh2);
        index3 = find(volume>volumeTh3);
        index4 = find(volume>volumeTh4);
        endPoint1=frame2sampleIndex([index1(1), index1(end)], frameSize, overlap);
        endPoint2=frame2sampleIndex([index2(1), index2(end)], frameSize, overlap);
        endPoint3=frame2sampleIndex([index3(1), index3(end)], frameSize, overlap);
        endPoint4=frame2sampleIndex([index4(1), index4(end)], frameSize, overlap);

        figure(1)
        subplot(4,1,1);
        time=(1:length(y))/fs;
        plot(time, y);
        ylabel('Amplitude'); title('Waveform');
        axis([-inf inf -1 1]);
        legend('Waveform', 'Boundaries by threshold 1', 'Boundaries by threshold 2', 'Boundaries by threshold 3', 'Boundaries by threshold 4');

        subplot(4,1,2);
        frameTime=frame2sampleIndex(1:frameNum, frameSize, overlap);
        time=(1:length(y))/fs;
        plot(frameTime/44100, volume, '.-');
        ylabel('Sum of Abs.'); title('Volume');
        axis tight;
        legend('Volume', 'Threshold 1', 'Threshold 2', 'Threshold 3', 'Threshold 4');

        subplot(4,1,3);
        nfft = 2^nextpow2(fs); % n-point DFT
        numUniq = ceil((nfft + 1)/2); % half point
        f = (0:numUniq - 1)' * fs / nfft; % frequency vector (one sided)
        myRecordingFFT = fft(y, nfft);
        n = length(y) / 2; % bc complex conjugates pairs we only need half
        amp_spec = 20*log10(abs(myRecordingFFT)) - 20*log10(n);
        plot(f, abs(amp_spec(1:numUniq)))
        xlabel('Frequency (Hz)'), ylabel('Magnitude (dB)')
        axis([0 5000 0 max(abs(amp_spec))])

        % Add time-frequency plot
        subplot(4,1,4);
        window = hamming(frameSize);
        noverlap = overlap;
        [s, f_spec, t_spec, ps] = spectrogram(y, window, noverlap, [], fs);
        [max_power, max_index] = max(ps);
        dominant_freq = f_spec(max_index);
        plot(t_spec, dominant_freq, '.-');
        ylabel('Frequency (Hz)'); xlabel('Time (s)');
        title('Time-Frequency plot (Dominant Frequency)');
        ylim([0 5000]); % Limit frequency axis to 0-5000 Hz
        h = figure(1);
        exportgraphics(h,'pic.png')


    end
end

